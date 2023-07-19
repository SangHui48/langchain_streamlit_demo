import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config, ConfigBuilder
from githubqa.get_info_from_api import github_api_call, ROOT
from anytree import RenderTree 


def load_graph_data():
    nodes = []
    edges = []
    
    total_info_dict, _ = github_api_call("https://github.com/SamLynnEvans/Transformer")
    
    for _, _, tmp_node in RenderTree(ROOT):
        
        nodes.append(
             Node(id=tmp_node.name,
                  label=tmp_node.name,
                 shape="circularImage",
                image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png"
                 )
            )
        if tmp_node.parent:
            edges.append(
                Edge(source=tmp_node.parent.name, target=tmp_node.name, label="")
            )

    return nodes, edges

nodes, edges = load_graph_data()

config = Config(width=750,
                height=950,
                directed=True, 
                physics=True, 
                hierarchical=True,
                # **kwargs
                )

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

# 1. Build the config (with sidebar to play with options) .
config_builder = ConfigBuilder(nodes)
config = config_builder.build()

# 2. If your done, save the config to a file.
config.save("config.json")

# 3. Simple reload from json file (you can bump the builder at this point.)
config = Config(from_json="config.json")