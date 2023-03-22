FROM continuumio/miniconda3:4.9.2
RUN conda install -c psi4/label/dev -c conda-forge \
    psi4 \
    dftd3 \
    mp2d \
    qcengine \
    qcfractal \
    rdkit \
    geometric \
    uvicorn-standard \
    fastapi \
    xtb \
    xtb-python 

COPY manager.yml /etc/qcfractal-manager/manager.yaml

RUN groupadd -g 999 qcfractal && \
    useradd -m -r -u 1000 -g qcfractal qcfractal
ENV PATH /opt/local/conda/envs/base/bin/:$PATH

WORKDIR /app

COPY . ./

USER root
RUN touch /app/manager.log
RUN chmod -R a+rwx /app

USER qcfractal

EXPOSE 7860

ENTRYPOINT ["/app/entrypoint.sh"]