FROM odoo:11

USER root

COPY ./requirements.txt /

RUN pip3 install -r requirements.txt

USER odoo