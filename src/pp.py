import pandas as pd
import numpy as np
import csv

HAPPY_COL_FORMAT = ['GT', 'QQ', 'BD', 'BK', 'BI', 'BVT', 'BLT']
TVC_COL_FORMAT = []

HAPPY_FILE = "/Users/jj/PycharmProjects/little_ds_problem/data/3140_03.happy.AmpliSeq.Clean.vcf"
TVC_FILE = "/Users/jj/PycharmProjects/little_ds_problem/data/3140_03.TVC.GRCh37.clean.vcf"



def clean_happy_file(file):
    with open(file, "r") as f:
        r = csv.DictReader(f, delimiter="\t")
        l = []
        for row in r:
            f = row["FORMAT"].split(":")
            t = row["TRUTH"].split(":")
            q = row["QUERY"].split(":")

            n_dict = {}
            for i in HAPPY_COL_FORMAT:

                if i in f:
                    t_value = t[f.index(i)]
                    q_value = q[f.index(i)]

                    if isFloat(t_value):
                        t_value = float(t_value)

                    if isFloat(q_value):
                        q_value = float(q_value)

                    if t_value == ".":
                        t_value = None
                    if q_value == ".":
                        q_value = None

                    n_dict.update({"T_" + i: t_value, "Q_" + i: q_value})
                else:
                    t_value = None
                    q_value = None

                    n_dict.update({"T_" + i: t_value, "Q_" + i: q_value})


            row.update(n_dict)

            l.append(row)


        df = pd.DataFrame(l)

        cols = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'TRUTH', 'QUERY', 'T_BD',
                'T_BI', 'T_BK', 'T_BLT', 'T_BVT', 'T_GT', 'T_QQ', 'Q_BD', 'Q_BI', 'Q_BK', 'Q_BLT', 'Q_BVT', 'Q_GT',
                'Q_QQ']

        df = df[cols]
        return df



TVC_FORMAT = ["GT", "GQ", "DP", "RO", "AO", "SRF", "SRR", "SAF", "SAR", "FDP", "FRO", "FAO",
              "AF", "FSRF", "FSRR", "FSAF", "FSAR"]

TVC_INFO = ["NS", "HS", "DP", "RO", "AO", "SRF", "SRR", "SAF", "SAR", "FDP", "FRO", "FAO", "AF", "QD", "FSRF",
 "FSRR", "FSAF", "FSAR", "FXX", "TYPE", "LEN", "HRUN", "FR", "RBI", "FWDB", "REVB", "REFB", "VARB",
 "SSSB", "SSEN", "SSEP", "STB", "STBP", "PB", "PBP", "MLLD", "OID", "OPOS", "OREF", "OALT", "OMAPALT"]

TVC_ORIGINAL = ["CHROM", "POS", "ID", "REF", "ALT",	"QUAL",	"FILTER", "INFO", "FORMAT",	"3140_3"]






def get_TVC_file(file):
    with open(file, "r") as f:
        r = csv.DictReader(f, delimiter="\t")
        l = []

        for row in r:
            if row["INFO"]:
                info = row["INFO"].split(";")
                i_dict = {}

                for i in info:
                    kv = i.split("=")
                    if len(kv) == 2:
                        if kv[1] == ".":
                            i_dict.update({kv[0]: None})
                        else:
                            i_dict.update({kv[0]: kv[1]})
                    elif len(kv) == 1:
                        i_dict.update({kv[0]: None})

                for i in TVC_INFO:
                    if i in i_dict.keys():
                        pass
                    else:
                        i_dict.update({i: None})



            if row["FORMAT"]:
                format = row["FORMAT"].split(":")
                format_3140 = row["3140_3"].split(":")
            else:
                format = []

            f_dict = {}
            for i in TVC_FORMAT:
                if i in format:
                    format_3140[format.index(i)]
                    f_dict.update({'f_'+i: format_3140[format.index(i)]})
                else:
                    f_dict.update({'f_'+i: None})

            row.update(i_dict)
            row.update(f_dict)
            l.append(row)


        df = pd.DataFrame(l)

        cols = ['CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', '3140_3',  'AF',
                'AO',  'DP', 'FAO', 'FDP', 'FR', 'FRO', 'FSAF', 'FSAR', 'FSRF', 'FSRR', 'FWDB', 'FXX',
                'HRUN', 'HS',   'LEN', 'MLLD', 'NS', 'OALT', 'OID', 'OMAPALT', 'OPOS', 'OREF', 'PB', 'PBP', 'QD',
                'RBI', 'REFB', 'REVB', 'RO', 'SAF', 'SAR', 'SRF', 'SRR', 'SSEN', 'SSEP', 'SSSB', 'STB', 'STBP',
                'TYPE', 'VARB', 'f_AF', 'f_AO', 'f_DP', 'f_FAO', 'f_FDP', 'f_FRO', 'f_FSAF', 'f_FSAR', 'f_FSRF',
                'f_FSRR', 'f_GQ', 'f_GT', 'f_RO', 'f_SAF', 'f_SAR', 'f_SRF', 'f_SRR']

        df = df[cols]
        return df









# tvc_df = get_TVC_file(TVC_FILE)
#
# print(tvc_df)

# happy_df = clean_happy_file(HAPPY_FILE)
#
#
# print(len(tvc_df))
# print(len(happy_df))
#
#
#
# tvc_df.to_csv("tvc_mod.vcf", sep='\t')
# happy_df.to_csv("happy_mod.vcf", sep='\t')
#
# m_df = pd.merge(tvc_df, happy_df, how='inner', on=['CHROM', 'POS', 'REF', 'ALT'])
# d_df = m_df.drop_duplicates()
#
#
# d_df.to_csv("tvc_mod.vcf", sep="\t")


def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False



def clean_TVC(file):
    with open(file, "r") as f:
        r = csv.DictReader(f, delimiter="\t")
        l = []

        for row in r:
            info = row["INFO"].split(";")
            format = row["FORMAT"]
            tvc_3140_3 = row["3140_3"].split(":")

            tis = ["ti_"+ti for ti in TVC_INFO]

            info_dict = dict.fromkeys(tis)

            for i in info:
                kv = i.split("=")
                k = kv[0]
                v = kv[1]
                if isFloat(v):
                    v = float(v)
                else:
                    if v == '.':
                        v = None

                info_dict.update({"ti_" + k: v})

            format_dict = {}
            if format:
                f = format.split(":")
                for i in TVC_FORMAT:
                    if i in f:
                        index = f.index(i)
                        k = i
                        v = tvc_3140_3[index]
                        if isFloat(v):
                            v = float(v)
                        format_dict.update({"tf_" + k: v})
                    else:
                        format_dict.update({"tf_" + k: None})
            else:
                for i in TVC_FORMAT:
                    format_dict.update({"tf_" + i: None})

            # print(info_dict)
            # print(format_dict)

            row.update(info_dict)
            row.update(format_dict)

            l.append(row)

        df = pd.DataFrame(l)

    # reordering the columns
    tf = ["tf_" + t for t in TVC_FORMAT]
    ti = ["ti_" + t for t in TVC_INFO]
    df = df[TVC_ORIGINAL + tf + ti]

    # info, format and ID will be dropped.
    df = df.drop(['ID', 'FORMAT', 'INFO', '3140_3'], axis=1)


    return df



tvc_df = clean_TVC(TVC_FILE)
# print(tvc_df)
# tvc_df.to_csv("tvc_mod.vcf", sep="\t")


h_df = clean_happy_file(HAPPY_FILE)
h_df = h_df.drop(['ID', 'QUAL', 'FILTER', 'INFO', 'FORMAT', 'TRUTH', 'QUERY'], axis=1)
h_df.to_csv("happy_mod.vcf", sep="\t")


# print(h_df)

m_df = pd.merge(tvc_df, h_df, how='inner', on=['CHROM', 'POS', 'REF', 'ALT'])

m_df.to_csv("merged.vcf", sep='\t')











