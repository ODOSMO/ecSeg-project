import os


def ref_inf( ref_dir, lib_name='library', lib_out_name='ref-dist-mat', kmer = 31):
    # todo: refernce_dir location
    os.system('skmer reference {r} -p 4 -l {ln} -o {lon} -k {k}'.format(r=ref_dir,ln=lib_name,lon=lib_out_name, k=kmer) )
    
def dis_inf( lib, jc_name='jc-dist-mat' ):
    #lib_path = os.getcwd()
    os.system('skmer distance {l} -t -o {o}'.format(l = lib, o = jc_name))

def query_inf( username, result_path, query, lib_path, a=False, prefix = 'dist' ): #use path to insert query and lib
    rp = result_path + '/' + username
    qname = os.path.basename(query).rsplit('.f', 1)[0]
    cmd = ''
    if a == False:
	# matrix file to result/username/
	# query_output to result/username/
	p = os.path.join(rp,prefix)
	cmd = 'python ./mysite/core/skmer/__main__.py query {q} {l} -O {rp} -o {p}'.format(q=query,l=lib_path+'/'+username, rp=rp, p = p)
	out_dat = os.path.join(rp+'/'+qname, qname+'.dat')
    else:
	# matrix file to result/username/
	# query_output to database/username/
	p = os.path.join(rp,prefix)
	cmd = 'python ./mysite/core/skmer/__main__.py query {q} {l} -a -o {p}'.format(q=query,l=lib_path+'/'+username, p = p)
	out_dat = os.path.join(lib_path+'/'+username+'/'+qname, qname+'.dat')
    os.system(cmd)
    out_matrix = os.path.join(rp, prefix+'-q1.txt')
    print [out_dat,out_matrix]
    return [out_dat,out_matrix]

if __name__ == '__main__':
    query_inf( 'test', 'result','query/test/q1.fastq','database')
