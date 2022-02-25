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
    #print("\t\t\t" + b + "  " + x)
    if b == x:
        score = 1 - e
       # print("\t\t\t" + str(score))
        return score
    score = e/3
    #print("\t\t\t" + str(score))
    return score
        

def likelihood_of_genotypes(bases):
    diploid_genotypes = [('A','A'), ('C','C'), ('G','G'), ('T','T'), ('A','C'), ('A','G'), ('A','T'), ('C','G'), ('C','T'), ('G','T')]
    scores = []
    best_genotype = [('X','Y')]
    best_score = 0
    for G in diploid_genotypes:
        score = 1.0
        for base in bases:
            score = score * b_given_X_Y(base, G[0], G[1])
            #print("\t" + str(base)+ "  "  + str(G) + "  "  + str(score))
        
        if score > best_score:
            best_score = score
            best_genotype = [G]

        if (score == best_score) & (G not in best_genotype):
            best_genotype.append(G)
    
        #genotype_tup = (G[0], G[1], score)
        #scores.append(genotype_tup)
    #scores_sorted = scores.sort(key=lambda i:i[2])
    #print(scores)
    #print(best_genotype)
    #print(str(best_score) + "\n" + str(math.log(best_score)))
    return (best_genotype, math.log(best_score))


def likelihood_of_cancer(bases, G):
    score = 1.0
    best_score = 0
    for base in bases:
        for g in G:
            score = score * b_given_X_Y(base, g[0], g[1])
            if score < best_score:
                best_score = score
        #print("\t" + str(base)+ "  "  + str(G) + "  "  + str(score))

    return (math.log(score))


def find_somatic(cancer_bam, normal_bam):
    n_list = []
    c_list = []

    for ncol in normal_bam.pileup():
        n_list.append(ncol)

    suff_coverage = []
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
            for nread in ncol.pileups:
                nbase = nread.alignment.query_sequence[nread.query_position]
                #print(str(len(nread.alignment.query_sequence))+ "    " + str(nread.query_position) )
                nbases.append(nbase)
            #print("coverage: " + str(n_coverage) +"length of list: " + str(len(nbases)))
            cbases = []
            for read in col.pileups:
                base = read.alignment.query_sequence[read.query_position]
                cbases.append(base)
            best_genotype, best_score = likelihood_of_genotypes(nbases)
            if best_score < -50:
                print("Postiion " + str(pos) + " has ambiguous genotype.")
            else:
                somatic_score = likelihood_of_cancer(cbases, best_genotype)
                print(somatic_score)
                if somatic_score < -75:
                    print("Position " + str(pos) + " has a candidate somatic mutation (Log-likelihood= " + str(somatic_score) + ")")
            


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

    

            

        
    
