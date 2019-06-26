import webbrowser
import os
import interface
import project_cluster
import pandas as pd

def output( username, result_path, query, lib_path, a=False, prefix='dist', kmer=31 ):
    qname = os.path.basename(query).rsplit('.f', 1)[0]
    paths = interface.query_inf( username, result_path, query, lib_path, a, prefix )
    image_url = os.path.abspath(project_cluster.draw_tree(paths[1]))
    # get repeat content and genome size
    in_file = open(paths[0], 'r')
    genome_size = 0.0
    repeat = []
    for line in in_file.readlines():
	l = line.split()
	if 'genome_length' in l:
		genome_size = l[1]
	if 'repeat_profile' in l:
		repeat = [l[1],l[2],l[3],l[4],l[5]]
    repeat = [float(x)*100 for x in repeat]
    # get the taxonomical info
    df = pd.read_csv(paths[1],sep='\t')
    df.drop(df.tail(1).index,inplace=True)
    sp_idx = df[qname].idxmin()
    specie = df['sample'].values[df[qname].idxmin()]
    distance = df.at[sp_idx,qname]
    # generate html page
    outpage_path = os.path.abspath(result_path)+'/'+username+'/'+qname+'.html'
    f = open(outpage_path,'w')
    style = ''' <style>
    table { font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}
    td, th {border: 1px solid #dddddd;text-align: left;padding: 8px; width:100%;}
    tr:nth-child(even) {background-color: #dddddd;}
    </style>'''
    message = """<!DOCTYPE html><html>
    {st}
    <h1>{q} Result</h1>
    <body><table>
	  <tr>
	    <th colspan = "3">Attribution</th>
	    <th colspan = "3">Content</th>
	  </tr>
	  <tr>
	    <th colspan = "3">K-mer size</th>
	    <td colspan = "3">{k}</td>
	  </tr>
	    <th colspan = "3">Query genome size (bp)</th>
	    <td colspan = "3">{g}</td>
	  </tr>
	  <tr>
	    <th rowspan="2" color bgcolor="#FFFFFF">Repeat content of genome(%) corresponding to kmer</th>
	    <th>Once</th>
	    <th>Twice</th>
	    <th>3 times</th>
	    <th>4 times</th>
	    <th>5 times</th>
	  </tr>
	  <tr>
	    <td>{r1}</td>
	    <td>{r2}</td>
	    <td>{r3}</td>
	    <td>{r4}</td>
	    <td>{r5}</td>
	  </tr>
	  <tr>
	    <th colspan = "2">Distance from the taxonomically closest genome (Exp(mutation per nucleotide))</th>
	    <td colspan = "2">{sp}</td>
	    <td colspan = "2">{ds}</td>
	  </tr>
	</table>
	<center><img src = {ip} style='height: 100%; width: 100%; object-fit: contain' /></center></body>
    </html>""".format( ip = image_url, k = kmer, g=genome_size, q=qname, r1=repeat[0], r2=repeat[1],r3=repeat[2],r4=repeat[3],r5=repeat[4], sp=specie,ds=distance, st= style)

    f.write(message)
    f.close()

    filename = 'file:///'+outpage_path
    webbrowser.open_new_tab(filename)

if __name__ =='__main__':
    output( 'test', 'result', 'query/test/q1.fastq', 'database')
