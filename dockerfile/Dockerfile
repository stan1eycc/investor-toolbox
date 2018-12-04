FROM continuumio/anaconda3:latest

# Install Jupyter
RUN /opt/conda/bin/conda install --yes --quiet jupyter && \
    mkdir /opt/notebooks

# Install Pandas Datareader
RUN /opt/conda/bin/conda install --yes --quiet pandas-datareader

RUN /opt/conda/bin/conda clean -tipsy && \ 
