import pysam
import argparse
import math

def b_given_X_Y(b, x, y):
    p_x = b_given_X(b,x)
    p_y = b_given_X(b,y)

    ret = 0.5*p_x + 0.5*p_y
    return ret


def b_given_X(b, x):
    e = 0.1
    if b == x:
        score = 1.000 - e
    else:
        score = e/3.0
    return score
        

def likelihood_of_genotypes(bases):
    diploid_genotypes = [('A','A'), ('C','C'), ('G','G'), ('T','T'), ('A','C'), ('A','G'), ('A','T'), ('C','G'), ('C','T'), ('G','T')]
    best_genotype = {}
    for G in diploid_genotypes:
        score = 1.0
        for base in bases:
            score = b_given_X_Y(base.upper(), G[0], G[1])
            key = ''.join(G)
            if key not in best_genotype:
                best_genotype[key] = 1.0

            best_genotype[key] *= score
        
    max_key = max(best_genotype, key = best_genotype.get)
    #print(best_genotype)
    best_score = math.log(best_genotype[max_key])
    return (max_key, best_score)


def likelihood_of_cancer(bases, G):
    best_score = 1.0
    
    for base in bases:
        score = b_given_X_Y(base.upper(), G[0], G[1])
        best_score *= score

    log_score = math.log(best_score)
    return (log_score)


def find_somatic(cancer_bam, normal_bam):

    c_tot = 0
    n_tot = 0
    suff_coverage = []
    for (col, ncol) in zip(cancer_bam.pileup(), normal_bam.pileup()):
        
        pos = col.pos

        c_coverage = col.n
        n_coverage = ncol.n

        c_tot += c_coverage
        n_tot += n_coverage
        
        if (n_coverage < 20) | (c_coverage < 20):
            print("Insufficient coverage at position: " + str(pos))
        else:
            suff_coverage.append(pos)
            
            nbases = []
            num_bases = 0
            
            for nread in ncol.pileups:
                nbase = nread.alignment.query_sequence[nread.query_position]
                num_bases += len(nread.alignment.query_sequence)
                nbases.append(nbase.upper())

                
            cbases = []
            for read in col.pileups:
                base = read.alignment.query_sequence[read.query_position]
                cbases.append(base.upper())
            
            best_genotype, best_score = likelihood_of_genotypes(nbases)
            if best_score < -50:
                print("Position " + str(pos) + " has ambiguous genotype.")
                
            else:
                somatic_score = likelihood_of_cancer(cbases, best_genotype)
                if somatic_score < -75:
                    print("Position " + str(pos) + " has a candidate somatic mutation (Log-likelihood= " + str(somatic_score) + ")")            
          

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", required=True, type=str, help="input the normal bam file location")
    parser.add_argument("-c",required=True, type=str, help="input the cancer bam file location")
    args = parser.parse_args()
    try:
        cancer_bam = pysam.AlignmentFile(args.c)
    except Exception:
        print("An invalid cancer bam file was input, please check filenames and try again.")
    try:
        normal_bam = pysam.AlignmentFile(args.n)
    except Exception:
        print("An invalid normal bam file was input, please check filenames and try again.")
        
    find_somatic(cancer_bam, normal_bam)

    

            

        
    
