# coding=utf-8
from flask import Flask, render_template, request, redirect, url_for
import pymysql
import networkx as nx
import matplotlib
matplotlib.use('Agg') # this allows PNG plotting
import matplotlib.pyplot as plt
import tempfile
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from networkx.readwrite import json_graph
import json
import numpy as np



dbname="conceptmap"
host="localhost"
user="root"
passwd=""
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

trans_dic={			u'台湾':u'Taiwan',\
                    u'民主':u'Democracy',\
                    u'国民党':u'Kuomintang',\
                    u'政治':u'Politics',\
                    u'大陆':u'Mainland',\
                    u'选举':u'Election',\
                    u'民进党':u'DPP',\
                    u'体制':u'FormOfGovernment',\
                    u'中国':u'China',\
                    u'价值':u'Value',\
                    u'社会':u'Society',\
                    u'普世':u'Universal',\
                    u'政府':u'Government',\
                    u'国家':u'Country',\
                    u'经济':u'Economy',\
                    u'媒体':u'Media',\
                    u'人民':u'People',\
                    u'民众':u'People',\
                    u'制度':u'Institution',\
                    u'香港':u'Hongkong',\
                    u'选民':u'Voter',\
                    u'发展':u'Development',\
                    u'选举人':u'Voter',\
                    u'学生':u'Student',\
                    u'自由':u'Freedom',\
                    u'历史':u'History',u'Otherwords':u'Otherwords',\
                    u'公民':u'Citizen',\
                    u'美国':u'USA',\
                    u'道德':u'Ethics',\
                    u'利益':u'Benefit',\
                    u'权力':u'Power',\
                    u'政策':u'Policy',\
                    u'总统':u'President',\
                    u'俄罗斯':u'Russia',\
                    u'腐败':u'Corruption',\
                    u'日本':u'Japan',\
                    u'国会':u'Congress',\
                    u'独裁':u'Dictatorship',\
                    u'印度':u'India',\
                    u'权利':u'Right',\
                    u'独立':u'Independent',\
                    u'宪法':u'Constitution',\
                    u'三权分立':u'SepOf3Powers'
                    }




app = Flask(__name__)
@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))




@app.route('/<name>/')
def make_country_resp(name):
	en_to_chinese_dic={
		'NorthKorea':'朝鲜',
		'Japan':'日本',\
		'India':'印度',\
		'Singapore':'新加坡',\
		'Russia':'俄罗斯',\
		'Taiwan':'台湾',\
		'Hongkong':'香港',\
		'USA':'美国'
		}
	cur = db.cursor()
	sql = "SELECT answerId, keyword, sentenceindex FROM keywords_democracy where country= '%s';" % en_to_chinese_dic[name]
	cur.execute(sql)
	keywords_list=[] #for network draw
	keywords_dic={}  #count the frequency of keywords
	for tup in cur.fetchall():
		keywords_list.append(tup)
		if not keywords_dic.has_key(tup[1]):
			keywords_dic[tup[1]]=1
		else:
			keywords_dic[tup[1]] +=1
	keywords_dic_en={}
	for item in keywords_dic.items():
		keywords_dic_en[trans_dic[item[0]]]=item[1]
	'''get network
	'''
	edge_list = get_edgelist(keywords_list)
	sender_dic={}
	for item in edge_list:
		tie=item[0]+'/'+item[1]
		if not tie in sender_dic.keys():
			sender_dic[tie]=1
		else:
			sender_dic[tie]=sender_dic[tie]+1
	sender_dic_en={}  #translate into english 
	for item in sender_dic.items():
		new_key = trans_dic[item[0].split('/')[0]]+'/'+trans_dic[item[0].split('/')[1]]
		sender_dic_en[new_key]=item[1]
	#print sender_dic_en.keys()

	nodes_list=[]
	for key in sender_dic_en.keys():
		string1,string2 = key.split('/')
		if not string1 in nodes_list:
			nodes_list.append(string1)
		if not string2 in nodes_list:
			nodes_list.append(string2)

	edge_list_en=[]
	for item in sender_dic_en.items():
		edge_list_en.append((item[0].split('/')[0],item[0].split('/')[1],item[1]))
	'''draw network
	'''
	G1=nx.Graph()
	G1.add_nodes_from(nodes_list)
	G1.add_weighted_edges_from(edge_list_en)
	elarge=[(u,v) for (u,v,d) in G1.edges(data=True) if d['weight'] <=100]
	esmall=[(u,v) for (u,v,d) in G1.edges(data=True) if d['weight'] >=1000]
	pos = nx.shell_layout(G1)
	width=[]
	for (u,v,d) in G1.edges(data=True):
		width.append(d.values()[0])
	

	frequency_list=[]
	for value in keywords_dic_en.values():
		frequency_list.append(value)
	heights,edges = np.histogram(frequency_list)
	p = figure(title='Keywords frequency: '+name)
	p.quad(top=heights,bottom=0,left=edges[:-1],right=edges[1:],fill_color="orange",line_color="black")
	figJS,figDiv = components(p,CDN)

	nx.draw_networkx_nodes(G1,pos,node_color='white',node_size=1200)
	nx.draw_networkx_edges(G1,pos,edgelist=elarge,width=width)
	nx.draw_networkx_edges(G1,pos,edgelist=esmall,width=width,alpha=0.5,edge_color='b',style='dashed')
	nx.draw_networkx_labels(G1,pos,font_size=10,font_family='sans-serif')
	f2="F:\\cfss\\cfss-homework-newllqllz\\final_project\\static\\"+name+".png"
	#f = tempfile.NamedTemporaryFile(dir='static/temp',suffix='.png',delete=False)
	plt.savefig(f2)
	plt.clf()

	return render_template('keywords.html',keywords_dic=keywords_dic_en,figJS=figJS,figDiv=figDiv,name=name)#figJS=figJS,figDiv=figDiv






def get_edgelist(cutwords_list):
    new_edge_list=[]

    WEIGHT = 1
    
    for i in range(len(cutwords_list)):
        print i
        if i>0:
            if cutwords_list[i-1][0]==cutwords_list[i][0]:#if keywords in the same answer
                
                if not too_far_away(cutwords_list[i-1][2],cutwords_list[i][2]):
                    sender = cutwords_list[i-1][1]
                    sender_index=cutwords_list[i-1][2]
                    receiver = cutwords_list[i][1]
                    receiver_index=cutwords_list[i][2]
                    weight=WEIGHT
                    if not (sender_index==receiver_index):
                        new_edge_list.append((sender,receiver,weight))
    return new_edge_list


def too_far_away(previous_index, current_index):
    too_faraway=True
    distance=3  #可以调整，距离以内表示有影响
    if current_index-previous_index<=distance:
        too_faraway=False
    return too_faraway


if __name__ == '__main__':
	# en_to_chinese_dic={'NorthKorea':'朝鲜',
 #    	'Japan':'日本',\
 #    	'India':'印度',\
 #    	'Singapore':'新加坡',\
 #    	'Russia':'俄罗斯',\
 #    	'Hongkong':'香港',\
 #    	'USA':'美国'}
	# cur = db.cursor()
	# print en_to_chinese_dic['Japan']
	# sql = "SELECT answerId, keyword, sentenceindex FROM keywords_democracy where country= '%s';" % en_to_chinese_dic['Japan']
	# cur.execute(sql)
    #print type('中国')
    app.debug=True
    app.run()
    
    	
