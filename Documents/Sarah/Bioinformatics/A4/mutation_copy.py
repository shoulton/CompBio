import pysam
import argparse
import math

def b_given_X_Y(b, x, y):
    p_x = b_given_X(b,x)
    p_y = b_given_X(b,y)

    ret = 0.5*p_x + 0.5*p_y
    #print("\t\t" + str(ret))
    return ret


def b_given_X(b, x):
    e = 0.1
    #print("\t\t\t" + b + "  " + x)
    if b != x:
        return e / 3.0
    else:
        return 1.000 - e

def likelihood_of(bases, geno, pp):
    best_genotype = {}
    for GG in geno:
        score = 1.0
        for base in bases:
            score = b_given_X_Y(base.upper(), GG[0], GG[1])
            key = GG
            if key not in best_genotype:
                best_genotype[key] = 1.0

            best_genotype[key] *= score

    max_key = max(best_genotype, key = best_genotype.get)
    best_score = math.log(best_genotype[max_key])
    #print(best_score)
    return (best_score, [max_key])



def find_somatic(cancer_bam, normal_bam):
    n_list = []
    c_list = []

    for ncol in normal_bam.pileup():
        n_list.append(ncol)        

    suff_coverage = []
    ncol= {}
    for col in cancer_bam.pileup():
        c_list.append(col)
        pos = col.pos
        ncol = n_list[pos]

        c_coverage = col.n
        n_coverage = ncol.n
       
        if (n_coverage < 20) | (c_coverage < 20):
            print("Insufficient coverage at position: " + str(pos))
        else:
            suff_coverage.append(pos)

    nbases = []
    for nread in normal_bam.pileup():
        pos = nread.pos
        if pos in suff_coverage:
            nbases = nread.get_query_sequences()

            diploid_genotypes = [('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T'), (
                'A', 'C'), ('A', 'G'), ('A', 'T'), ('C', 'G'), ('C', 'T'), ('G', 'T')]
            genotype = ('AA', 'CC', 'GG', 'TT', 'AC','AG', 'AT', 'CG', 'CT', 'GT')
            best_score, best_genotype = likelihood_of(nbases, diploid_genotypes, pos)
            if best_score < -50:
                    print("Postiion " + str(pos) + " has ambiguous genotype.")
                    continue
            else:
                #print(pos, best_genotype)
                for ccol in cancer_bam.pileup():
                    if ccol.pos != pos:
                        continue
                    else:
                        cbases = ccol.get_query_sequences()
                        somatic_score, xx = likelihood_of( cbases, best_genotype, pos)
                        if somatic_score < -75:
                            print(pos)
    #    #pos = nread.query_position
    #    print(nread)
    #    break



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", required=True, type=str, help="input the normal bam file location")
    parser.add_argument("-c",required=True, type=str, help="input the cancer bam file location")
    args = parser.parse_args()
    try:
        cancer_bam = pysam.AlignmentFile(args.c)
        normal_bam = pysam.AlignmentFile(args.n)
    except Exception:
        print("An invalid file was input, please check filenames and try again.")
    find_somatic(cancer_bam, normal_bam)