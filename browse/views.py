
import os
import random
import string
import subprocess
from django.shortcuts import render
from django.db import connection


path_get = os.getcwd()


def name_set():
    c = ''.join(random.sample(string.digits, 9))
    os.mkdir(f"file_keep/{c}")
    return c


def write_fasta_file(query_sequence, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    temp_fasta_file = os.path.join(output_directory, "temp_query.fasta")
    with open(temp_fasta_file, "w") as f:
        current_gene_id = None
        current_sequence = ""
        for line in query_sequence.split("\n"):
            if line.startswith(">"):
                if current_gene_id and current_sequence:
                    f.write(f">{current_gene_id}\n{current_sequence}\n")
                current_gene_id = line.strip()[1:]
                current_sequence = ""
            else:
                current_sequence += line.strip()
        if current_gene_id and current_sequence:
            f.write(f">{current_gene_id}\n{current_sequence}\n")
    return temp_fasta_file


def run_blastp(query_file, nucl_or_prot, species_data, evalue, output_file):
    print({os.path.dirname(query_file)})
    cmd = f"""
    source /etc/profile
    cd {os.path.dirname(query_file)}
    blastn -query {query_file} -db {path_get}/static/blast_match_database/{nucl_or_prot}/RiceLncRNA.db -outfmt 6 -evalue {evalue} -out {output_file} -num_threads 2
    """
    subprocess.run(cmd, shell=True)


def parse_blastp_result(blast_result_file):
    blast_results = []
    with open(blast_result_file, "r") as f:
        for line in f:
            fields = line.strip().split("\t")
            blast_results.append((fields[0], fields[1], float(fields[2]), int(fields[3]), int(fields[4]), int(fields[5]), int(fields[6]), int(fields[7]), int(fields[8]), int(fields[9]), f"{float(fields[10]):.2e}", f"{float(fields[11]):.2e}"))
    subject_ids = [result[1] for result in blast_results]
    return blast_results, subject_ids


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')


def jbrowse(request):
    return render(request, 'jbrowse.html')


def blast(request):
    return render(request, 'blast.html')

def blast_run(request):
    sp_data_1 = request.POST.get("sp_data_1")
    # geneid = request.POST.get('geneid')
    query_sequence = request.POST.get('query_sequence')

    # if sp_data_1 is None or geneid is None:
    if sp_data_1 is None or query_sequence is None:
        return render(request, 'blast.html')

    if query_sequence:
        c = name_set()
        output_directory = f"{path_get}/file_keep/{c}"
        temp_fasta_file = write_fasta_file(query_sequence, output_directory)

        nucl_or_prot = "nucl"
        species_data = sp_data_1
        e = "1e-5"
        blast_result_file = os.path.join(output_directory, "result.txt")
        run_blastp(temp_fasta_file, nucl_or_prot, species_data, e, blast_result_file)
        blast_results, geneids = parse_blastp_result(blast_result_file)

    return render(request, '../templates/blast.html', {
        'blast_results': blast_results if query_sequence else None  # 如果没有查询序列，则不返回 blast_results
    })



def table_lncRNA(request):
    return render(request, 'table_lncRNA.html')

def table_lncRNA_run(request):
    sp_data_1 = request.POST.get("sp_data_1")
    geneid = request.POST.get('geneid')
    print(sp_data_1, geneid)

    if sp_data_1 is None or geneid is None:
        return render(request, 'table_lncRNA.html')

    geneids = geneid.replace('\r', '').split('\n')
    print(geneids)
    # 查询数据库
    geneid_placeholders = ','.join(['%s'] * len(geneids))
    sql_query = f"SELECT * FROM rice_table WHERE Attributes IN ({geneid_placeholders})"
    with connection.cursor() as cursor:
        cursor.execute(sql_query, geneids)  # 重复两次以匹配 OR 条件中的参数数量
        result = cursor.fetchall()
    connection.close()

    return render(request, '../templates/table_lncRNA.html', {'result': result})


def download(request):
    return render(request, 'download.html')


def statistics1(request):
    return render(request, 'statistics1.html')

def statistics1(request):
    return render(request, 'statistics1.html')

def statistics2(request):
    return render(request, 'statistics2.html')


def documentation(request):
    return render(request, 'documentation.html')


def submit(request):
    return render(request, 'submit.html')


def contact(request):
    return render(request, 'contact.html')
