FROM continuumio/miniconda3

WORKDIR /home/biolib

RUN conda install --yes -c r r 
RUN conda install --yes pytorch scikit-learn pandas numpy \
    && conda clean -afy

RUN R -e "install.packages('protr',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages('Peptides',dependencies=TRUE, repos='http://cran.rstudio.com/')"

COPY . .

ENTRYPOINT [ "python", "src/predict.py" ]
