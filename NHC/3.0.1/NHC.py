#!/usr/bin/env python
# python3.8
__author__ = "Peng Zhang"
__copyright__ = "Laboratory of Human Genetics of Infectious Diseases, The Rocefeller Unversity"
__license__ = "CC BY-NC-ND 4.0"
__version__ = "verion-3, 2024-02"


import os
import time
import argparse
from scipy import stats
import rpy2
import rpy2.robjects as ro
from decimal import Decimal
from collections import defaultdict
from datetime import datetime

###
# (1) Input Parameters
###

print('\n---------------------------------------')
print('   ###    ##   ##     ##     ######    ')
print('   ## #   ##   ##     ##    ##    ##   ')
print('   ##  #  ##   #########   ##          ')
print('   ##   # ##   ##     ##    ##    ##   ')
print('   ##    ###   ##     ##     ######    \n')
print(' Network-based Heterogenity Clustering ')
print('---------------------------------------\n')

global_start = time.time()
parser = argparse.ArgumentParser(description="Network-based Heterogenity Clustering")
parser.add_argument("-path", help="absolute path of the input files")
parser.add_argument("-input", help="input file for samples, genes and variants [check test_input.txt]")
parser.add_argument("-pc", help="three principal components for all samples [check test_pc.txt]")
parser.add_argument("-mode", type=int, default=1, help="(default=1), 1 for case-only analysis; 2 for case-vs-control analysis")
parser.add_argument("-edge", type=float, default=0.99, help="(default=0.99), edge weight cutoff, range: 0.7~1")
parser.add_argument("-hub", type=int, default=100, help="(default=100), remove hub genes with high connectivity, use 0 to keep all genes")
parser.add_argument("-merge", type=float, default=0.5, help="(default=0.5), merge overlapped gene clusters, range: 0~1")
parser.add_argument("-boost", type=str, default='N', help="(default=N), Y or N to use boost version")
parser.add_argument("-network", type=str, default='N', help="(default=N), Y or N to generate network files for visualization")
parser.add_argument("-suffix", help="suffix of output folder")
parser.add_argument("-data", help="Absolute path to data folder contain reference files for NHC.")

args = parser.parse_args()
path = args.path
filename_input = args.input
filename_pc = args.pc
mode = args.mode
edge_cutoff = args.edge
hub_cutoff = args.hub
merge_cutoff = args.merge
boost = args.boost
network = args.network
suffix = args.suffix
# This is the directory to the data folder
# containing the reference files for NHC
# such as the Data_NHC_Network_Connectivity.txt
# Data_NHC_Network.txt, Data_NHC_Geneset.txt
# etc.
data = os.path.abspath(args.data)

year = str(datetime.now().year)
month = str(datetime.now().month)
day = str(datetime.now().day)
hour = str(datetime.now().hour)
minute = str(datetime.now().minute)
second = str(datetime.now().second)
timestamp = year+'-'+month+'-'+day+'-'+hour+'-'+minute+'-'+second

if path[-1] != '/':
	path = path + '/'
output_folder = 'NHC_output'+'_'+suffix
os.system('mkdir -p '+path+output_folder)

file_parameter = open(path+output_folder+'/NHC_input_parameters.txt', 'w')
file_parameter.write('---------------------------------------\n')
file_parameter.write('   ###    ##   ##     ##     ######    \n')
file_parameter.write('   ## #   ##   ##     ##    ##    ##   \n')
file_parameter.write('   ##  #  ##   #########   ##          \n')
file_parameter.write('   ##   # ##   ##     ##    ##    ##   \n')
file_parameter.write('   ##    ###   ##     ##     ######    \n')
file_parameter.write(' Network-based Heterogenity Clustering \n')
file_parameter.write('---------------------------------------\n\n')
file_parameter.write('NHC Parameters\n\n')
file_parameter.write('Path: ' + path + '\n')
file_parameter.write('Input: ' + filename_input + '\n')
file_parameter.write('PC: ' + filename_pc + '\n')
file_parameter.write('Mode: ' + str(mode) + '\n')
file_parameter.write('Edge-Weight Cutoff: ' + str(edge_cutoff) + '\n')
file_parameter.write('Hub-Gene Cutoff: ' + str(hub_cutoff) + '\n')
file_parameter.write('Cluster-Merge Cutoff: ' + str(merge_cutoff) + '\n')
file_parameter.write('Boost: ' + boost + '\n')
file_parameter.write('Network: ' + network + '\n')
file_parameter.write('Suffix: ' + suffix + '\n')
file_parameter.write('Output: ' + path + output_folder + '\n')


###
# (2) Loading Data
###
print('>> Loading Data\n')

file_input = open(path + filename_input, 'r')
input_header = file_input.readline()
case_set = set()
case_gene_set = set()
case_gene_set_dict = defaultdict(set)
case_gene_var_set_dict = defaultdict(lambda: defaultdict(set))
ctl_set = set()
ctl_gene_set_dict = defaultdict(set)
for eachline in file_input:
	item = eachline.strip().split('\t')
	group = item[0]
	sample = item[1]
	gene = item[2]
	var = '\t'.join(item[3:])
	if group == 'case':
		case_set.add(sample)
		case_gene_set.add(gene)
		case_gene_set_dict[sample].add(gene)
		case_gene_var_set_dict[sample][gene].add(var)
	elif group == 'control':
		ctl_set.add(sample)
		ctl_gene_set_dict[sample].add(gene)
case_list = list(case_set)
case_list.sort()
ctl_list = list(ctl_set)
ctl_list.sort()
file_input.close()


file_pc = open(filename_pc, 'r')
file_pc.readline()
pc_dict = dict()
for eachline in file_pc:
	item = eachline.strip().split('\t')
	sample = item[0]
	pc1 = item[1]
	pc2 = item[2]
	pc3 = item[3]
	pc_dict[sample] = pc1 + '\t' + pc2 + '\t' + pc3
file_pc.close()


file_connectivity = open(os.path.join(data, 'Data_NHC_Network_Connectivity.txt'), 'r')
hub_gene_set = set()
for eachline in file_connectivity:
	item = eachline.strip().split('\t')
	gene = item[0]
	connectivity = int(item[1])
	if connectivity >= hub_cutoff:
		hub_gene_set.add(gene)
file_connectivity.close()


file_network = open(os.path.join(data, 'Data_NHC_Network.txt'), 'r')
case_network_dict = dict()
for eachline in file_network:
	item = eachline.strip().split('\t')
	geneA = item[0]
	geneB = item[1]
	gene_pair = (geneA, geneB)
	edge = float(item[2])
	if (geneA in case_gene_set) and (geneB in case_gene_set) and (edge >= edge_cutoff):
		if hub_cutoff == 0:
			case_network_dict[gene_pair] = edge
		else:
			if (geneA not in hub_gene_set) and (geneB not in hub_gene_set):
				case_network_dict[gene_pair] = edge
file_network.close()


file_enrichment = open(os.path.join(data, 'Data_NHC_Geneset.txt'), 'r')
database_list = ['MSigDB_Hallmark','KEGG_Pathway','Reactome_Pathway','Wiki_Pathway',
				'GO_BiologicalProcess','GO_MolecularFunction']
database_gene_set_dict = defaultdict(set)
database_term_gene_set_dict = defaultdict(lambda: defaultdict(set))
for eachline in file_enrichment:
	item = eachline.strip().split('\t')
	database = item[0]
	term = item[1]
	gene_set = set(item[3].split(','))
	database_gene_set_dict[database] = database_gene_set_dict[database] | gene_set
	database_term_gene_set_dict[database][term] = gene_set
file_enrichment.close()


###
# (3) Gene Clustering
###
print('>> Gene Clustering')

global_clusters = set()
global_cluster_result = list()
global_case_gene_visited = set()
file_out_initial = open(path+output_folder+'/temp_clusters_initial.txt', 'w')


# function for gene clustering
def gene_clustering(cur_index):
	cur_case = case_list[cur_index]
	cur_case_gene_set = case_gene_set_dict[cur_case]
	for cur_gene in cur_case_gene_set:
		this_gene_set = set()
		this_gene_set.add(cur_gene)
		this_case_set = set()
		this_case_set.add(cur_case)
		checking_index_set = set(range(len(case_list)))
		checking_index_set.remove(cur_index)

		while checking_index_set:
			closest_index = -1
			closest_case = ''
			closest_gene = ''
			overlap = False
			highest_edge = 0
			for checking_index in checking_index_set:
				checking_case = case_list[checking_index]
				checking_gene_set = case_gene_set_dict[checking_case]
				overlap_gene_set = this_gene_set & checking_gene_set
				if overlap_gene_set:
					closest_index = checking_index
					closest_case = checking_case
					overlap = True
					break
				else:
					for existing_gene in this_gene_set:
						for checking_gene in checking_gene_set:
							if existing_gene < checking_gene:
								checking_pair = (existing_gene, checking_gene)
							else:
								checking_pair = (checking_gene, existing_gene)
							temp_edge = 0
							if checking_pair in case_network_dict.keys():
								temp_edge = case_network_dict[checking_pair]
							if temp_edge > highest_edge:
								closest_index = checking_index
								closest_case = checking_case
								closest_gene = checking_gene
								highest_edge = temp_edge

			if overlap:
				checking_index_set.remove(closest_index)
				this_case_set.add(closest_case)
			elif closest_index != -1:
				checking_index_set.remove(closest_index)
				this_case_set.add(closest_case)
				this_gene_set.add(closest_gene)
			else:
				break

		if len(this_gene_set) > 2:
			this_gene_cluster_list = list(this_gene_set)
			this_gene_cluster_list.sort()
			this_gene_cluster_output = ';'.join(this_gene_cluster_list)
			this_case_cluster_list = list(this_case_set)
			this_case_cluster_list.sort()
			this_case_cluster_output = ';'.join(this_case_cluster_list)
			if this_gene_cluster_output not in global_clusters:
				global_clusters.add(this_gene_cluster_output)
				this_cluster_result = (str(len(this_gene_set))+'\t'+this_gene_cluster_output+'\t'+
									   str(len(this_case_set))+'\t'+this_case_cluster_output)
				global_cluster_result.append(this_cluster_result)


# function for gene clustering (boost)
def gene_clustering_boost(cur_index):
	cur_case = case_list[cur_index]
	cur_case_gene_set = case_gene_set_dict[cur_case]
	for cur_gene in cur_case_gene_set:
		this_gene_set = set()
		this_case_set = set()
		cur_case_gene = cur_case + ':' + cur_gene
		if cur_case_gene not in global_case_gene_visited:
			global_case_gene_visited.add(cur_case_gene)
			this_gene_set.add(cur_gene)
			this_case_set.add(cur_case)
			checking_index_set = set(range(len(case_list)))
			checking_index_set.remove(cur_index)

			while checking_index_set:
				closest_index = -1
				closest_case = ''
				closest_gene = ''
				overlap = False
				highest_edge = 0
				for checking_index in checking_index_set:
					checking_case = case_list[checking_index]
					checking_gene_set = case_gene_set_dict[checking_case]
					overlap_gene_set = this_gene_set & checking_gene_set
					if overlap_gene_set:
						closest_index = checking_index
						closest_case = checking_case
						overlap = True
						break
					else:
						for existing_gene in this_gene_set:
							for checking_gene in checking_gene_set:
								checking_case_gene = checking_case + ':' + checking_gene
								if checking_case_gene not in global_case_gene_visited:
									if existing_gene < checking_gene:
										checking_pair = (existing_gene, checking_gene)
									else:
										checking_pair = (checking_gene, existing_gene)
									temp_edge = 0
									if checking_pair in case_network_dict.keys():
										temp_edge = case_network_dict[checking_pair]
									if temp_edge > highest_edge:
										closest_index = checking_index
										closest_case = checking_case
										closest_gene = checking_gene
										highest_edge = temp_edge

				if overlap:
					checking_index_set.remove(closest_index)
					this_case_set.add(closest_case)
					for each_overlapping_gene in overlap_gene_set:
						closest_case_gene = closest_case + ':' + each_overlapping_gene
						global_case_gene_visited.add(closest_case_gene)
				elif closest_index != -1:
					checking_index_set.remove(closest_index)
					this_case_set.add(closest_case)
					this_gene_set.add(closest_gene)
					closest_case_gene = closest_case + ':' + closest_gene
					global_case_gene_visited.add(closest_case_gene)
				else:
					break

		if len(this_gene_set) > 2:
			this_gene_cluster_list = list(this_gene_set)
			this_gene_cluster_list.sort()
			this_gene_cluster_output = ';'.join(this_gene_cluster_list)
			this_case_cluster_list = list(this_case_set)
			this_case_cluster_list.sort()
			this_case_cluster_output = ';'.join(this_case_cluster_list)
			if this_gene_cluster_output not in global_clusters:
				global_clusters.add(this_gene_cluster_output)
				this_cluster_result = (str(len(this_gene_set))+'\t'+this_gene_cluster_output+'\t'+
									   str(len(this_case_set))+'\t'+this_case_cluster_output)
				global_cluster_result.append(this_cluster_result)


# running gene clustering for all cases
for case_i in range(len(case_list)):
	start = time.time()
	if boost == 'N':
		gene_clustering(case_i)
	elif boost == 'Y':
		gene_clustering_boost(case_i)
	end = time.time()
	timecost = str(round(end-start, 3))
	print('   '+str(case_i+1)+'/'+str(len(case_list))+' '+case_list[case_i]+' ('+timecost+' sec)')
print('   # Gene Clusters (initial): '+str(len(global_cluster_result))+'\n')

for each_cluster in global_cluster_result:
	file_out_initial.write(each_cluster + '\n')
file_out_initial.close()


###
# (4) Gene Cluster Merging
###
print('>> Gene Cluster Merging')

gene_cluster_merging = list()
case_cluster_merging = list()
for each_cluster in global_cluster_result:
	gene_cluster_merging.append(set(each_cluster.split('\t')[1].split(';')))
	case_cluster_merging.append(set(each_cluster.split('\t')[3].split(';')))
file_out_merged = open(path+output_folder+'/temp_clusters_merged.txt', 'w')

stable = False
while not stable:
	N = len(gene_cluster_merging)
	overlap_max = 0
	overlap_max_pair = [-1, -1]
	overlap_all_in = False
	for i in range(0, N):
		for j in range(i+1, N):
			if gene_cluster_merging[i].issubset(gene_cluster_merging[j]):
				overlap_max_pair = [i, j]
				overlap_max = 1
			elif gene_cluster_merging[j].issubset(gene_cluster_merging[i]):
				overlap_max_pair = [i, j]
				overlap_max = 1
			else:
				intersect = len(gene_cluster_merging[i] & gene_cluster_merging[j])
				union = len(gene_cluster_merging[i] | gene_cluster_merging[j])
				overlap_ratio = round(float(intersect) / float(union), 3)
				if overlap_ratio > overlap_max:
					overlap_max_pair = [i, j]
					overlap_max = overlap_ratio

	if overlap_max >= merge_cutoff:
		stable = False
		max_i = overlap_max_pair[0]
		max_j = overlap_max_pair[1]

		new_gene_cluster_merging = gene_cluster_merging[max_i] | gene_cluster_merging[max_j]
		gene_cluster_merging.append(new_gene_cluster_merging)
		gene_cluster_merging[max_i] = set()
		gene_cluster_merging[max_j] = set()

		new_case_cluster_merging = case_cluster_merging[max_i] | case_cluster_merging[max_j]
		case_cluster_merging.append(new_case_cluster_merging)
		case_cluster_merging[max_i] = set()
		case_cluster_merging[max_j] = set()

		temp_gene_cluster_merging = list()
		for each_gene_cluster_merging in gene_cluster_merging:
			if each_gene_cluster_merging:
				temp_gene_cluster_merging.append(each_gene_cluster_merging)
		gene_cluster_merging = temp_gene_cluster_merging

		temp_case_cluster_merging = list()
		for each_case_cluster_merging in case_cluster_merging:
			if each_case_cluster_merging:
				temp_case_cluster_merging.append(each_case_cluster_merging)
		case_cluster_merging = temp_case_cluster_merging

	else:
		stable = True

if stable:
	for k in range(0, len(gene_cluster_merging)):
		merged_gene_cluster_list = list(gene_cluster_merging[k])
		merged_gene_cluster_list.sort()
		merged_gene_cluster_output = ';'.join(merged_gene_cluster_list)
		merged_case_cluster_list = list(case_cluster_merging[k])
		merged_case_cluster_list.sort()
		merged_case_cluster_output = ';'.join(merged_case_cluster_list)
		file_out_merged.write(str(len(merged_gene_cluster_list))+'\t'+merged_gene_cluster_output+'\t'+
							  str(len(merged_case_cluster_list))+'\t'+merged_case_cluster_output+'\n')
print('   # Gene Clusters (merged): '+str(len(gene_cluster_merging))+'\n')
file_out_merged.close()


###
# (5) Gene Cluster Enrichment
###
print('>> Gene Cluster Enrichment')

file_in_merged = open(path+output_folder+'/temp_clusters_merged.txt', 'r')
file_output = open(path+output_folder+'/NHC_output_gene_clusters.txt', 'w')
file_output.write('Cluster\tGene_Count\tGene_Cluster\tCase_Count\tCase_Cluster\tCluster_pvalue\t'
				  'MSigDB_Hallmark\tKEGG_Pathway\tReactome_Pathway\tWiki_Pathway\t'
				  'GO_BiologicalProcess\tGO_MolecularFunction\n')

cluster_id = 0
gene_cluster_enriched_set = set()
for eachline in file_in_merged:
	start = time.time()
	cluster_id += 1
	output_cluster_info = 'Cluster_' + str(cluster_id) + '\t' + eachline.strip()
	item = eachline.strip().split('\t')
	this_cluster_gene_set = set(item[1].split(';'))
	this_case_list = item[3].split(';')

	output_cluster_pvalue = '.'
	if mode == 2:
		this_ctl_list = list()
		for each_ctl in ctl_gene_set_dict.keys():
			if len(this_cluster_gene_set & ctl_gene_set_dict[each_ctl]) > 0:
				this_ctl_list.append(each_ctl)
	
		file_temp_PC = open('temp_pc.txt', 'w')
		file_temp_PC.write('ID\tPHENOTYPE\tPC1\tPC2\tPC3\tCARRIER\n')
		for each_case in case_list:
			if each_case in this_case_list:
				file_temp_PC.write(each_case + '\t1\t' + pc_dict[each_case] + '\t1\n')
			else:
				file_temp_PC.write(each_case + '\t1\t' + pc_dict[each_case] + '\t0\n')
		for each_ctl in ctl_list:
			if each_ctl in this_ctl_list:
				file_temp_PC.write(each_ctl + '\t0\t' + pc_dict[each_ctl] + '\t1\n')
			else:
				file_temp_PC.write(each_ctl + '\t0\t' + pc_dict[each_ctl] + '\t0\n')
		file_temp_PC.close()
	
		ro.r("data <- read.table('temp_pc.txt', header=T, sep='\t')")
		ro.r("fit <- glm(data=data, PHENOTYPE ~ PC1+PC2+PC3+CARRIER, family='binomial')")
		ro.r("adjusted.pval <- anova(fit, test='LRT')[5, 5]")
		r_pvalue = ro.r("adjusted.pval")
		pvalue = r_pvalue[0]
		pvalue = float('%.3E' % Decimal(pvalue))
		output_cluster_pvalue = str(pvalue)


	output_cluster_enrichment = ''
	for each_database in database_list:
		enrichment_hit = dict()
		database_gene_set = database_gene_set_dict[each_database]
		database_term_list = database_term_gene_set_dict[each_database].keys()
		database_term_size = len(database_term_list)

		for each_term in database_term_list:
			term_gene_set = database_term_gene_set_dict[each_database][each_term]
			cluster_in_term_in = this_cluster_gene_set & term_gene_set
			cluster_in_term_out = this_cluster_gene_set - cluster_in_term_in
			cluster_out_term_in = term_gene_set - cluster_in_term_in
			cluster_out_term_out = database_gene_set - this_cluster_gene_set - term_gene_set
			if len(cluster_in_term_in) != 0:
				odd, pvalue = stats.fisher_exact([[len(cluster_in_term_in), len(cluster_in_term_out)],
												  [len(cluster_out_term_in), len(cluster_out_term_out)]],
												 alternative='two-sided')
				adj_pvalue = pvalue * database_term_size
				if adj_pvalue < 0.00001:
					adj_pvalue = float('%.3E' % Decimal(adj_pvalue))
					enrichment_hit[each_term] = adj_pvalue

		if len(enrichment_hit) == 0:
			output_cluster_enrichment += '.\t'
		elif len(enrichment_hit) > 0:
			gene_cluster_enriched_set.add(cluster_id)
			enrichment_hit_sorted = sorted(enrichment_hit.items(), key=lambda x: x[1])
			enrichment_output = ''
			for each_sorted in enrichment_hit_sorted:
				term = each_sorted[0]
				pvalue = each_sorted[1]
				enrichment_output += term + ' (' + str(pvalue) + ');'
			output_cluster_enrichment += enrichment_output[0:-1] + '\t'
	output_cluster_enrichment = output_cluster_enrichment[0:-1]
	file_output.write(output_cluster_info+'\t'+output_cluster_pvalue+'\t'+output_cluster_enrichment+'\n')

	end = time.time()
	timecost = str(round(end-start, 3))
	print('   ' + str(cluster_id)+'/'+str(len(gene_cluster_merging))+' ('+timecost+' sec)')

print('   # Gene Clusters (enriched): '+'\t'+str(len(gene_cluster_enriched_set))+'\n')
file_in_merged.close()
file_output.close()

###
# (7) Extracting Variants for Each Cluster
###
print('>> Extracting Variants for Each Cluster\n')

os.system('mkdir -p '+path+output_folder+'/variant_files')
file_cluster = open(path+output_folder+'/NHC_output_gene_clusters.txt', 'r')
file_cluster.readline()
for eachline in file_cluster:
	item = eachline.strip().split('\t')
	cluster_id = item[0].lower()
	gene_cluster = item[2].split(';')
	case_cluster = item[4].split(';')

	file_var = open(path+output_folder+'/variant_files/NHC_output_gene_'+cluster_id+'_variants.txt', 'w')
	file_var.write(input_header)
	for each_gene in gene_cluster:
		for each_case in case_cluster:
			var_set = case_gene_var_set_dict[each_case][each_gene]
			if var_set:
				for each_var in var_set:
					file_var.write('case\t'+each_case+'\t'+each_gene+'\t'+each_var+'\n')
file_cluster.close()


###
# (7) Generating Network Files
###
if network == 'Y':
	print('>> Generating Network Files\n')

	os.system('mkdir -p '+path+output_folder+'/network_files')
	file_cluster = open(path+output_folder+'/NHC_output_gene_clusters.txt', 'r')
	file_cluster.readline()
	for eachline in file_cluster:
		item = eachline.strip().split('\t')
		cluster_id = item[0].lower()
		gene_cluster = item[2].split(';')
		case_cluster = item[4].split(';')

		file_network = open(path+output_folder+'/network_files/NHC_output_gene_'+cluster_id+'_network.csv', 'w')
		for each_gene_pair in case_network_dict:
			geneA = each_gene_pair[0]
			geneB = each_gene_pair[1]
			if (geneA in gene_cluster) and (geneB in gene_cluster):
				file_network.write(geneA + '\t' + geneB + '\n')

		file_node = open(path+output_folder+'/network_files/NHC_output_gene_'+cluster_id+'_node.csv', 'w')
		file_node.write('ID\tCase_Count\tVar_Count\n')
		for each_gene in gene_cluster:
			case_count = 0
			var_count = 0
			for each_case in case_cluster:
				if each_gene in case_gene_set_dict[each_case]:
					case_count += 1
					var_count += len(case_gene_var_set_dict[each_case][each_gene])
			file_node.write(each_gene+'\t'+str(case_count)+'\t'+str(var_count)+'\n')
file_cluster.close()


###
# (8) The End
###

global_end = time.time()
global_timecost = str(round(global_end-global_start, 3))
print('>> Total Time Cost:'+'\t'+global_timecost+' sec\n')

os.remove(path+output_folder+'/temp_clusters_initial.txt')
os.remove(path+output_folder+'/temp_clusters_merged.txt')
if mode == 2:
	os.remove('temp_pc.txt')
