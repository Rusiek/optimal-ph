
import pandas as pd
import re

def extract_motif(word):
    """
    Extract motif and qvalue from 1 line
    Returns tuple: (motif, qvalue)
    """
    
    exp= '^Name=[0-9]+\-([A-Z]+).+qvalue=\s([0-9\.]+)'
    motif_qvalue = re.match(exp, word)
    return motif_qvalue.groups()

def parseFimo(file: str, qvalue_filter=0.05) -> pd.DataFrame:
    

    data = pd.read_csv(file, skiprows=1, sep='\t',header=None)

    data = data[[0,8]].rename(columns={0:'Seq_name', 8:'Info'})

    data['motif_qvalue'] = data.Info.apply(extract_motif)

    data[['motif', 'qvalue']] = pd.DataFrame(data.motif_qvalue.tolist(), index=data.index)

    data.drop(['Info', 'motif_qvalue'],axis=1, inplace=True)

    data.qvalue = data.qvalue.apply(pd.to_numeric)

    data = data[data['qvalue'] > qvalue_filter]

    motifs = list(data.motif.unique())

    index = [f'Seq{i}' for i in range(1,105002)]

    data_out = pd.DataFrame(columns=motifs, index=index)

    for mot in motifs:
        data_out[mot] = data_out.index.isin(data.loc[data.motif == mot, "Seq_name"])

    data_out.replace({True:1, False:0}, inplace=True)
    
    return data_out

