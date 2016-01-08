FROM centos:centos7
MAINTAINER r2h2 <rainer@hoerbe.at>

# PVZD Administration System (PMP, PAtools)

RUN yum -y install epel-release
RUN yum -y groupinstall "Development Tools" "GNOME Desktop" net-tools
# boot into GNOME
RUN ln -sf /lib/systemd/system/runlevel5.target /etc/systemd/system/default.target

# Smarcard reader, Safenet Authentication Client
RUN yum -y install pcsc-lite
RUN mkdir -p /opt/sac/
ADD lib/safenet/Linux/Installation/Standard/RPM/x64/SafenetAuthenticationClient-9.0.43-0.x86_64.rpm /opt/sac/
RUN rpm -i /opt/sac/SafenetAuthenticationClient-9.0.43-0.x86_64.rpm --nodeps

# Install Java
RUN yum -y install java-1.8.0-openjdk-devel.x86_64
# Install MOA-ID

# Install Python for PolicyManager
# RHEL6: rh-python34 rh-python34-virtualenv etc.
RUN yum -y install python34-devel libffi-devel openssl-devel
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3.4 get-pip.py
RUN pip install cffi Cython future lxml pyOpenSSL gitdb GitPython json2html pytz requests simplejson

RUN git clone https://github.com/rhoerbe/PVZD.git
RUN echo "export JAVA_HOME=/etc/alternatives/java_sdk_1.8.0" >> /root/.bashrc
RUN echo "export JDK_HOME=/etc/alternatives/java_sdk_1.8.0" >> /root/.bashrc
RUN echo "export JRE_HOME=/etc/alternatives/java_sdk_1.8.0/jre" >> /root/.bashrc
cd pyjnius && python3.4 setup.py install
pip install
pip freeze

RUN systemctl enable  pcscd.service
RUN systemctl start  pcscd.service
