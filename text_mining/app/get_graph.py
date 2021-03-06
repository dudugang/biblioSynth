#!/usr/bin/env /usr/bin/python
# -*- coding: utf-8 -*-

# when more than one python exist in system, libraries might not be properly linked

import render
import util
import query
from random import choice
import string
from igraph.datatypes import UniqueIdGenerator
import igraph
import numpy as np


args = util.get_args()
render.http_header()
render.html_header()

max_vertices = 70
gt = args['GraphTerm'] if 'GraphTerm' in args else ''
#ct = args['ClusterTerm'] if 'ClusterTerm' in args else ''
mode = args['GraphMode'] if 'GraphMode' in args else ''
render.render_div_search(ft=gt, gt=gt) #display form
#render.render_datalist( 'terms');


if 'GraphTerm' in args and 'GraphMode' in args:
    graph_path = '/tmp/{}.svg'.format(''.join(choice(string.ascii_uppercase + string.digits) for _ in xrange(10)))
    render.render_div_search(gt=args['GraphTerm'], ft=args['GraphTerm'])
    render.render_datalist()
    if args['GraphMode'] == 'simple':
        pass
    elif args['GraphMode'] == 'complete':
        ids = UniqueIdGenerator()
        li =  query.get_cooccurrences(args['GraphTerm'])[:max_vertices]
        edge_list = [(ids[args['GraphTerm']], ids[term]) for (term,_) in li]
        weight_list = [float(w) for (_,w) in li]
        for i in xrange(len(li)):
            for j in xrange(i+1, len(li)):
                t1 = li[i][0]
                t2 = li[j][0]
                co = query.get_one_cooccurrence(t1, t2)
                if co:
                    edge_list.append((ids[t1], ids[t2]))
                    weight_list.append(float(co))
        g = igraph.Graph(edge_list, vertex_attrs=dict(name=ids.values()), edge_attrs=dict(weight=weight_list))
        L = g.es["weight"]
        w = L#weights
        mi = min(w)
        ma =  max(w)
        no = ma - mi
        w1 = np.array(L)
        w1 -= mi
        #w1 += 1
        w1 /= no
        w1 *= 10
        gs = g.community_walktrap()
        cl = gs.as_clustering()
        colors = ['#FFB6C1','#87CEFA','#90EE90', '#FF00FF','#FFFACD','#FFA07A', "#ED7BDC", "#B4E874", "#74C7E8", "#AE73E6"]
        igraph.plot(g, target='/Users/peter/Desktop/bar.svg', layout = g.layout("kamada_kawai"), vertex_label = g.vs["name"], vertex_color=[colors[i] for i in cl.membership], vertex_shape = ['triangle-up'] + max_vertices * ['circle'], edge_width = w1, edge_color='grey', bbox = (800,800))
        print graph_path
