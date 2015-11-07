1       Zweck
=============

Der PolicyManager implementiert einen Teil der Komponenten die im
Dokument „PV-ZD-ARCH“ beschreiben sind. Zweck der Implementierung ist
die Verwaltung von Zertifikate und SAML Metadaten nach PV-ZD-Policy,
abgebildet durch folgende Funktionen:

1.    Verwaltung der Rechte von Portaladministratoren in den zentralen
Diensten. Der PolicyManager implementiert den Use Case 3.2.1
„Portaladministrator melden“ [PV\_ZD\_ARCH]. Dabei übernimmt der
Depositar oder sein Vertreter die Meldungen von den
Portalverantwortlichen und fügt sie im Policy Directory. Um die
Berechtigung des Portaladministrators abzubilden, werden auch die
Organisationen der Portalbetreiber und ihre Domänen verwaltet.

2.    Rechteprüfung: Überprüfung der Autorisierung von Signaturen der
Meldungen von Portaladministratoren. Der PolicyManager implementiert den
Use Case 3.2.4 „Eigene Metadaten aktualisieren“, einschließlich der
Sonderfalles 3.2.5 „Key Rollover“

3.    Zertifikatssperre: Zertifikate, die einmal gesperrt wurden dürfen
nicht mehr erneut registriert werden. (Use Case 3.2.6 Zertifikate
widerrufen)

4.    Zertifikate aus SAML-Metadaten für R-Profil Portale übernehmen
(Use Case 3.4.2 Ablaufvariante 3.2)

2       Konzept
===============

Der PolicyManager Stelle drei Funktionen bereit:

​a. PMP – Policy Management Point für die Rechteverwaltung,
​b. PEP – Policy Enforcement Point für die Rechteprüfung und
​c. PA-Tool – Portaladmin Tool für Signatur von Metadaten und Extraktion
von Zertifikaten.

Der PMP erstellt ein Policy Directory und der PEP liest es um damit
Zugriffsentscheidungen zu treffen.

Das Policy Directory enthält die Liste der Portaladministratoren und
ihrer Rechte und wird durch den Depositar (oder seinen Vertreter)
gepflegt.

PATool hat drei Funktionen
a. createED: Erstellt aus einem X.509 Zertifikat einen EntityDescriptor (-\> R-Profil)
b. signED: Signiert einen EntityDescriptor (Xades enveloped)
c. extractED: extrahiert Zertifikate aus einem Metadaten-Aggregat

** **

3       PMP
===========

3.1      Datenmodell
--------------------

Um die Authentizität und Integrität des Policy Directory zu bestätigen
wird es vom Depositar signiert. Zusätzlich ist das Directory zur
Speicherung und Übermittlung als Journaldatei (append-only
Datenstruktur) aufgebaut. Dadurch kann es nur ergänzt werden, während
bestehende Einträge unverändert bleiben müssen.

Im Programm kommt das Policy Directory in 2 Varianten vor:

a. Journalisiert und signiert, (im Programm intern „aods“), und

b. konsolidiert (ohne gelöschte und aktualisierte Einträge, nach Suchschlüsseln sortiert) (im Programm intern „policyDict“ bezeichnet).

3.2      Abläufe
----------------

Im Policy Directory werden die Portalbetreiber, die von ihnen
verwalteten Domänen und die Portaladministratoren eingetragen. Es werden
folgende Abläufe unterstützt:

1.    Erstellung eines leeren Policy Directory

2.    Anfügen neuer Datensätze (als JSON Struktur oder via GUI);
Signieren mit der Bürgerkarte. Es können nur valide und gültig signierte
Policy Directory gelesen werden.

3.    Lesen und validieren des Policy Directory, Ausgabe als
JSON-Struktur die für die Verifikation der Rechte von
Portaladministratoren geeignet ist.

4.    Übermittlung des Policy Directory an Portalverantwortliche, damit
sie prüfen können welche Portaladministratoren aktuell bei ihnen
gemeldet sind.



3.3      Schnittstellen/Datenerfassung
--------------------------------------

Es gibt vier Recordtypen die zu erfassen sind:

a. **"domain"** (enthält eine Domain unter der Portale betrieben werden, z.B. bmi.gv.at oder pvawp.bmi.gv.at
b. **"organization"** (der Portalbetreiber)
c. **"revocation"** (ein gesperrtes Zertifikat eines Portals)
d. **"userprivilege"** (das Zertifikat einer Person der Zugriffsrechte eingeräumt werden)

Die Erfassung erfolgt mit „Input Records“ die in JSON notiert sind. Ein
Input File besteht aus einem Array mit aus folgender JSON-Struktur:

    [{"record": [\<record-type\>, \<primary key\>, \<attribut liste\>], "delete": false}]

    domain:
        \<primary key\> Domain Name
        Attribute 1: org-id (gvOuId der Organisation).

    organization:
        \<primary key\> org-id.
        Attribute 1: Name der Organisation

    revocation:
        \<primary key\> {Keytype} + Key. Implementiert ist KeyType = „cert“

    userprivilege:
        \<primary key\> {Keytype} + Key. Implementiert ist KeyType = „cert“
        Attribute 1:org-id
        Attribute 2: Name



3.4      Speicherformat
-----------------------

Die Speicherung mit Gewährleistung von Integrität und Authentizität
erfolgt mit einer Journaldatei (append-only data structure). Sie ist
hierarchisch aufgebaut, von innen nach außen wie folgt:
    
- Content Record: Record Type und die zugehörigen Attribute
- Wrapper Record: Hash Chain und Content Disposition.
  - Die Hash Chain beinhaltet pro Record einen Hashwert, der aus dem 
  JSON-codierten Content Record (UTF-8) und dem vorhergehenden Hashwert gebildet wird.
  - Die Content Disposition enthält das Delete Flag. Ist es True, wird
  ein vorhergehender Record mit dem gleichen Primary Key gelöscht, ist es False, 
  wird der Datensatz eingefügt (wenn der Primary Key nicht
  vorhanden ist) bzw. aktualisiert (wenn schon vorhanden).
- Journal: Liste von Wrapper-Records, die durch die Hash-Chain nur am Ende erweiterbar ist.

Das Journal wird in einer Datei vom PMP immer in folgender Weise gespeichert:
-  Bzip2-Kompression
-  Base64-Encoding
-  Enveloping XML Signature

![](PolicyManager%20Doku-Dateien/image002.png)
Wrapper: Hash Chain, delete flag, datestamp, userstamp

\

** **

4       PEP
===========

4.1      Konzept
----------------

Der PEP führt folgende Prüfungen pro Meldung durch:

1. Die Meldung (= SAML EntityDescriptor) ist konform zum XML Schema
2. Die Meldung ist konform zu den PVP2-Regeln (Schematron)
3. Die Meldung hat eine gültige Bürgerkarten-Signatur
4. Über den Public Key des Signators muss ein gültiger Portaladministrator gemeldet sein
5.    Der Portaladministrator muss berechtigt sein die im
EntityDescriptor enthaltenen Domänen zu verwalten. Dazu ist die
Beziehung userprivilege \<-\> organization \<-\> domain zu verwenden. Im
Detail ist zu prüfen, dass die Domain Namen in URLs von SAML
EntityDescriptors (EntitiyID, Endpoints) mit den berechtigten Domains
übereinstimmt. Als Übereinstimmung gilt, wenn der FQHN aus der
Berechtigung ganz oder teilweise im zu prüfenden FQHN enthalten ist.
6.    In der Meldung enthaltene Zertifikate müssen folgende Bedingungen
erfüllen:
  a. Nicht in der Sperrliste enthalten;
  b. CN-Komponente des x509subject Attributes ist eine Domäne die der Portaladministrator verwalten darf[[1]](#_ftn1);
  c. Der in x509NotValidAfter angegeben Zeitpunkt liegt in der Zukunft;
  d. Issuer in der Liste der akkreditierten CAs getrennt für STP/IDP und AWP/SP.

4.2      Schnittstelle für den Import und Weiterverarbeitung
------------------------------------------------------------

Die Kommunikation passiert über ein Git-Repository. Im Repository gibt
es drei Verzeichnisse, die jeweils dem Verarbeitungsstatus einer Meldung
entsprechen:

-  request\_queue (hier werden die XML-Dateien vom Depositar
eingestellt)
-       rejected (abgelehnte Meldungen plus Fehlermeldung)
-       accepted (aus diesem Verzeichnis erstellt der MD Aggregator das Aggregat)

Es werden 3 Instanzen des Repositories erstellt:
- Master (bare) zur Synchronisation
- Web (Upload der Meldungen/Download der Verarbeitungsberichte)
- Backend (Prüfung und Weitergabe an den MD-Aggregator)

Die Synchronisation der Instanzen Web und Backend mit der Master-Instanz
erfolgt über push/pull (Remote SSH)

Die Weiterverarbeitung über den Metadatenaggregator erfolgt über das
Verzeichnis „accepted“

Für die Aktualisierung einer Meldung muss eine Datei mit dem gleichen
Namen hochgeladen werden.

Für die Löschung einer Meldung muss eine EntityDescriptor hochgeladen
werden, der im Root-Element das Attribut
http://pvp.egov.gv.at:disposition = „True“ gesetzt hat.

\

* * * * *

[[1]](#_ftnref1) Es ist nicht notwendig, dass es sich um eine unter
einer ICANN-TLD registrierte Domain handelt (auch andere TLDs wie .intra
oder .local sind erlaubt)

