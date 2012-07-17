if (document.addEventListener) {
  document.addEventListener("DOMContentLoaded", init, false);
} else {
  window.onload = init;
}

const default_wordCloud = ld23_wordCloud;
const default_multiplatform = ld23_multiplatform;

const colors = {'osx': [10,255,255], 'web': [255,255,10], 'windows': [255,10,10], 'ios': [255,10,255], 'linux': [10,255,10], 'android':[50,50,255]};

var wordCloud = default_wordCloud;
var multiplatform = default_multiplatform;
var viewMode = "wordcloud";
var sigInst = null;
var hide = true;
var lastNode = null;
var showLabels = 1;

function init(){
	
	if(viewMode=="wordcloud")
		document.getElementById('stats').innerHTML = JSON.stringify(wordCloud.stats);
	else
		document.getElementById('stats').innerHTML = JSON.stringify(multiplatform.stats);
	
	// Instanciate sigma.js and customize rendering :
	sigInst = sigma.init(document.getElementById('sig'))
	//.debugMode(1)
	.drawingProperties({
		defaultLabelColor: '#fff',
	    defaultLabelSize: 14,
	    defaultLabelBGColor: '#fff',
	    defaultLabelHoverColor: '#000',
		labelSize: 'proportional',
		labelSizeRatio: 8,
	    labelThreshold: 0,
	    defaultEdgeType: 'curve',
	})
	.graphProperties({
	    minNodeSize: 0.5,
	    maxNodeSize: 20,
	    minEdgeSize: 1,
	    maxEdgeSize: 1
	})
	.mouseProperties({
	    maxRatio: 32,
		minRatio: 0.7,
		zoomDelta: 0.1,
		zoomMultiply: 2
		
	});

	// Generate graphe nodes and edges from JSON data

	/** WORD CLOUD **/
	if(viewMode == "wordcloud"){
		// . Nodes
		for(node in wordCloud.words){
			sigInst.addNode(wordCloud.words[node].label,
			{
				'x':Math.random(),
				'y':Math.random(),
				'label':wordCloud.words[node].label,
				'size':wordCloud.words[node].repetition,
				'color': 'rgb('+Math.round(Math.random()*256)+','+
								Math.round(Math.random()*256)+','+
								Math.round(Math.random()*256)+')'
			});
		}
		
		// . Edges
		var instance = 0;
		for(node in wordCloud.words){
			for( targetNode in wordCloud.words[node].edges){
				sigInst.addEdge(instance++,wordCloud.words[node].label,wordCloud.words[node].edges[targetNode]);
			}
		}
	}
	/** MULTIPLATFORM **/
	else{
		// . Nodes
		// .. Games
		for(node in multiplatform.games){
			
			c = computeColor(multiplatform.games[node].platforms);
			
			sigInst.addNode(multiplatform.games[node].uid,
			{
				'x':Math.random(),
				'y':Math.random(),
				'label':multiplatform.games[node].name,
				'size':multiplatform.games[node].platforms.length,
				'color': 'rgb('+c[0]+','+
								c[1]+','+
								c[2]+')'
			});
		}
		// .. Platforms
		for(node in multiplatform.stats){
		
			c = computeColor([node]);
			
			sigInst.addNode(node,
			{
				'x':Math.random(),
				'y':Math.random(),
				'label':node,
				'size':multiplatform.stats[node],
				'color': 'rgb('+c[0]+','+
								c[1]+','+
								c[2]+')'
			});
		}
		
		// . Edges
		var instance = 0;
		for(node in multiplatform.games){
			for( targetNode in multiplatform.games[node].platforms){
				sigInst.addEdge(instance++,multiplatform.games[node].uid,multiplatform.games[node].platforms[targetNode]);
				//sigInst.addEdge(instance++,multiplatform.games[node].platforms[targetNode],multiplatform.games[node].uid);
			}
		}
	}
	// Bind events :
	sigInst
	// . overnodes
/*	.bind('overnodes',function(event){
		
	})
*/	
	// . Click on a node
	.bind("upnodes", function (event) {
		var nodes = event.content;
		var neighbors = {};
		// Switch state if same node
		if(lastNode == String(nodes)){
			hide = !hide;
		}
		else
			hide = true;
		lastNode = nodes;
		// Hide
		if(hide){
		
			sigInst
			.iterEdges(function(e){
				if(nodes.indexOf(e.source)>=0 || nodes.indexOf(e.target)>=0){
					neighbors[e.source] = 1;
					neighbors[e.target] = 1;
			  }
			})
			.iterNodes(function(n){
				if(!neighbors[n.id]){
					n.hidden = 1;
				}else{
					n.hidden = 0;
				}
			}).draw(1,1,1,true);
		}else{
		
			sigInst
			.iterEdges(function(e){
				e.hidden = 0;
			})
			.iterNodes(function(n){
				n.hidden = 0;
			}).draw(1,1,1,true);			
		}
	});
	
	
	// UI
	// . ForceAtlas
	//sigInst.startForceAtlas2();
	var isRunning = false;
  	document.getElementById('stop-layout').addEventListener('click',function()
	{
		if(isRunning){
	    	isRunning = false;
	    	sigInst.stopForceAtlas2();
	    	document.getElementById('stop-layout').value = 'Start algorithm';
	    }else{
	    	isRunning = true;
	    	sigInst.startForceAtlas2();
	    	document.getElementById('stop-layout').value = 'Stop algorithm';
	    }
	},true);
	// Rescale graph
	document.getElementById('rescale-graph').addEventListener('click',function(){
			sigInst
			.iterEdges(function(e){
				e.hidden = 0;
			})
			.iterNodes(function(n){
				n.hidden = 0;
			})
			.graphProperties({
				minNodeSize: 0.5,
				maxNodeSize: 20,
				minEdgeSize: 1,
				maxEdgeSize: 1
			})
			.draw(1,1,1,true);
			// Reset current target
			lastNode = null;
	},true);
	// Hide/Show labels
	document.getElementById('label').addEventListener('click',function(){
		// Redraw 
		sigInst
			.graphProperties({
				minNodeSize: 5,// 0.5
				maxNodeSize: 5,
				minEdgeSize: 1,
				maxEdgeSize: 1
			})
			.draw(1,0,0,true);
	},true);
	
	
	
	// Draw the graph :
	sigInst.draw();
}

// Switch data set
function changeDataSet(dropdown){

	var index = dropdown.selectedIndex;
	var dataSet = dropdown.options[index].value;
	switch(dataSet){
		case "LD21":
		wordCloud = ld21_wordCloud;
		multiplatform = ld21_multiplatform;
		break;
		
		case "LD22":
		wordCloud = ld22_wordCloud;
		multiplatform = ld22_multiplatform;
		break;
		
		case "LD23":
		wordCloud = ld23_wordCloud;
		multiplatform = ld23_multiplatform;
		break;
		
		default:
		wordCloud = default_wordCloud;
		multiplatform = default_multiplatform;
	}
	// Stop sigmajs
	delete sigInst;
	document.getElementById('sig').innerHTML = "";
	// Start sigmajs again
	init();
}

// Switch data set
function changeViewMode(dropdown){

	var index = dropdown.selectedIndex;
	var dataSet = dropdown.options[index].value;
	switch(dataSet){
		case "wordcloud":
		viewMode = "wordcloud"; 
		break;
		
		case "multiplatform":
		viewMode = "multiplatform"; 
		break;
		
		default:
		viewMode = "wordcloud"; 
	}
	// Stop sigmajs
	delete sigInst;
	document.getElementById('sig').innerHTML = "";
	// Start sigmajs again
	init();
}

// Node color for the multiplatform visualization
function computeColor(platformList){
	
	var rf,gf,bf;
	var r,g,b;
	var firstIteration = 1;
	
	for(platform in platformList){
		r = colors[platformList[platform]][0];
		g = colors[platformList[platform]][1];
		b = colors[platformList[platform]][2];
		if(firstIteration-->0){
			rf = r;
			gf = g;
			bf = b;
		}
		// "Mixing" colors
		else{
			rf = (rf*r)/255;
			gf = (gf*g)/255;
			bf = (bf*b)/255;
		}
	}
	return [rf,gf,bf]
}



