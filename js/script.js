if (document.addEventListener) {
  document.addEventListener("DOMContentLoaded", init, false);
} else {
  window.onload = init;
}

function init(){
	
	// Instanciate sigma.js and customize rendering :
	var sigInst = sigma.init(document.getElementById('sig')).drawingProperties({
		defaultLabelColor: '#fff',
	    defaultLabelSize: 14,
	    defaultLabelBGColor: '#fff',
	    defaultLabelHoverColor: '#000',
	    labelThreshold: 6,
	    defaultEdgeType: 'curve'
	}).graphProperties({
	    minNodeSize: 0.5,
	    maxNodeSize: 20,
	    minEdgeSize: 1,
	    maxEdgeSize: 1
	}).mouseProperties({
	    maxRatio: 32
	});

	// Generate graphe nodes and edges from JSON data
	// . Nodes
	for(node in wordCloud.words){
		//console.log();
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
	
	// Bind events :
	sigInst.bind('overnodes',function(event){
		var nodes = event.content;
		var neighbors = {};
		sigInst.iterEdges(function(e){
	    	if(nodes.indexOf(e.source)>=0 || nodes.indexOf(e.target)>=0){
	        	neighbors[e.source] = 1;
	        	neighbors[e.target] = 1;
	      }
	    }).iterNodes(function(n){
	    	if(!neighbors[n.id]){
	    		n.hidden = 1;
	      	}else{
	        	n.hidden = 0;
	      	}
	    }).draw(2,2,2);
	}).bind('outnodes',function(){
		sigInst.iterEdges(function(e){
			e.hidden = 0;
		}).iterNodes(function(n){
			n.hidden = 0;
		}).draw(2,2,2);
	});
	
	// UI
	// . ForceAtlas
	sigInst.startForceAtlas2();
	var isRunning = true;
  	document.getElementById('stop-layout').addEventListener('click',function()
	{
		if(isRunning){
	    	isRunning = false;
	    	sigInst.stopForceAtlas2();
	    	document.getElementById('stop-layout').nodeValue = 'Start Layout';
	    }else{
	    	isRunning = true;
	    	sigInst.startForceAtlas2();
	    	document.getElementById('stop-layout').nodeValue = 'Stop Layout';
	    }
	},true);
	// Rescale graph
	document.getElementById('rescale-graph').addEventListener('click',function(){
	    sigInst.position(0,0,1).draw();
	},true);
	
	// Draw the graph :
	sigInst.draw();
}