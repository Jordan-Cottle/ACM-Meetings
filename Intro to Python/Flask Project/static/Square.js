
var gl;

var delay = 100;
var vertexCount;

var startVertex;
var maxVertices;
var drawCount = 3;

var drawMode;

var tracking = false;

window.onload = function init() {

    var canvas = document.getElementById( "gl-canvas" );
    
    gl = WebGLUtils.setupWebGL( canvas );
    if ( !gl ) { alert( "WebGL isn't available" ); }

    //
    //  Configure WebGL
    //
    gl.viewport( 0, 0, canvas.width, canvas.height );
    gl.clearColor( .95, .95, .95, 1.0);

    //  Load shaders and initialize attribute buffers
    
    var program = initShaders( gl, "vertex-shader", "fragment-shader" );
    gl.useProgram( program );

    const vertices = [
        vec2(0, 0),         //0
        vec2(  0,  .5 ),    //1
        vec2(.75, .75),     //2
        vec2(  .5,  0 ),    //3
        vec2(.75, -.75),    //4
        vec2(0,  -.5 ),     //5
        vec2(-.75, -.75),   //6
        vec2(-.5, 0),       //7
        vec2(  -.75, .75 ),  //8
    ]

    const indices =[
        // Fan 0-9
        0, 1, 2, 3, 4, 5, 6, 7, 8, 1,
            // Line loop 1-9
        
        // Triangles 10-27
        7, 8, 1, 
        1, 2, 3,
        3, 4, 5,
        5, 6, 7,
        7, 1, 5,
        5, 3, 1,

        // Triangle strip 28 - 37
        8, 7, 1, 2, 3, 7, 6, 5, 3, 4
    ];

    const fanStart = 0;
    const fanCount = 10;

    const lineStart = 1;
    const lineCount = 9;

    const triangleStart = 10;
    const triangleCount = 18;

    const stripStart = 28;
    const stripCount = 10;

    var vColors = [];

    // create random color for each vertex
    for(var i = 0; i < vertices.length; i++){
        var insert = vec4(
            Math.random(),
            Math.random(),
            Math.random(),
            1.0
        );
        vColors.push(insert);
    }

    // default mode is TRIANGLE_FAN
    startVertex = fanStart;
    maxVertices = fanCount;
    drawMode = gl.TRIANGLE_FAN;

    // Create a buffer to hold the  vertices
    var vBuffer = gl.createBuffer();

	// bind it to make it active
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);

	// send the data as an array to GL
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    				// Associate out shader variables with our data buffer

	// get a location to the vertex position's shader variable ('vPosition')
    var vPosition = gl.getAttribLocation( program, "vPosition");
	
	// specifies the vertex attribute information (in an array), used
	// for rendering 
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);

	// enable this attribute, with the given attribute name
    gl.enableVertexAttribArray(vPosition);

    // create color buffer
    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vColors), gl.STATIC_DRAW);

    // link color buffer to vColor attribute
    var vColor = gl.getAttribLocation(program, "vColor");
    gl.vertexAttribPointer(vColor, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vColor);

     // create color buffer
     var iBuffer = gl.createBuffer();
     gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, iBuffer);
     gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint8Array (indices), gl.STATIC_DRAW);
    
    
    // Initialize event handlers
    
    window.onkeydown = function(event) {
        var key = String.fromCharCode(event.keyCode);
        switch(key) {
            case '1': // select TRIANGLE_FAN drawing mode
                drawMode = gl.TRIANGLE_FAN;
                startVertex = fanStart;
                maxVertices = fanCount;
                delay = 150;
                break;
            case '2': // select LINE_LOOP drawing mode
                drawMode = gl.LINE_LOOP;
                startVertex = lineStart;
                maxVertices = lineCount;
                delay = 250;
                break;
            case '3': // select TRIANGLES drawing mode
                drawMode = gl.TRIANGLES;
                startVertex = triangleStart;
                maxVertices = triangleCount;
                delay = 75;
                break;
            case '4': // select TRIANGLE_STRIP drawing mode
                drawMode = gl.TRIANGLE_STRIP;
                startVertex = stripStart;
                maxVertices = stripCount;
                delay = 200;
                break;
            default:
                //console.log("Key pressed: " + key);
        }

        // start each mode with a single triangle
        drawCount = 3;

        // reset wait timer
        waitCount = 0;
    };

    

    window.addEventListener("mousedown", function() {
        canvas.addEventListener("mousemove", mouseMoveListener);
    });

    window.addEventListener("mouseup", function() {
        canvas.removeEventListener("mousemove", mouseMoveListener);
    });

    this.document.getElementById("worldCoordinateInput").addEventListener(
        "submit",
        updateCoordinates
    );

    // read default values of input tags into world coordinates
    updateCoordinates();

    dXMax = document.getElementById("gl-canvas").width;
    dYMax = document.getElementById("gl-canvas").height;

    this.console.log("Max device coordinates: (" + dXMax + ", " + dYMax + ")");
    render();
};

var waitCount = 0;
function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );

   // gl.drawArrays(drawMode, startVertex, drawCount);
    gl.drawElements(drawMode, drawCount, gl.UNSIGNED_BYTE, startVertex);

    // increase number of vertices up to max
    drawCount++;
    if(drawCount > maxVertices){
        drawCount = maxVertices;
        waitCount++;

        // then wait a bit before restarting
        if (waitCount > 8){
            drawCount = 3;
            waitCount = 0;
        }
    }
    
    setTimeout(
        function (){requestAnimFrame(render);}, delay
    );
}

// world min/max coordinates
var wXMin = 0;
var wYMin = 0;

var wXMax = 100;
var wYMax = 100;

// device min/max coordinates
var dXMin = 0;
var dYMin = 0;

var dXMax;
var dYMax;

function updateCoordinates(event){
    wXMin = Number(document.getElementById("xmin").value);
    wXMax = Number(document.getElementById("xmax").value);

    if(wXMin >= wXMax){
        alert("World x min must be greater than world x max!");
        let temp = wXMin;
        wXMin = wXMax;
        wXMax = temp;

        document.getElementById("xmin").value = wXMin;
        document.getElementById("xmax").value = wXMax;
    }

    wYMin = Number(document.getElementById("ymin").value);
    wYMax = Number(document.getElementById("ymax").value);

    if(wYMin >= wYMax){
        alert("World y min must be greater than world y max!");
        let temp = wYMin;
        wYMin = wYMax;
        wYMax = temp;

        document.getElementById("ymin").value = wYMin;
        document.getElementById("ymax").value = wYMax;
    }

    // Cancel form submission event, information is processed client-side
    if(event && event.cancelable){
        event.preventDefault();
    }
}

function displayToWorld(x, y){
    let deviceWidth = dXMax - dXMin;
    let worldWidth = wXMax - wXMin;

    let deviceHeight = dYMax - dYMin;
    let worldHeight = wXMax - wXMin;

    let xRatio = x / deviceWidth;
    let yRatio = y / deviceHeight;

    let result = [0 ,0];
    result[0] = (xRatio * worldWidth) + wXMin;
    result[1] = wYMax - (yRatio * worldHeight);

    return result;
}

function worldToNDC(x, y){

    let worldWidth = wXMax - wXMin;
    let worldHeight = wXMax - wXMin;

    let xRatio = (x-wXMin) / worldWidth;
    let yRatio = (y-wYMin) / worldHeight;

    var result = [0 ,0];
    result[0] = 2*xRatio - 1.0;
    result[1] = 2*yRatio - 1.0;

    return result;
}

function mouseMoveListener(event){
    var canvas = document.getElementById("gl-canvas");

    var rect = canvas.getBoundingClientRect();

    var x = event.clientX - rect.left;
    var y = event.clientY - (rect.top - .875);

    var coords = displayToWorld(x, y);
    var wX = coords[0];
    var wY = coords[1];

    coords = worldToNDC(wX, wY);
    var nX = coords[0];
    var nY = coords[1];

    var ndc_x = -1.0 + 2.0 * (x/canvas.width);
    var ndc_y =   1.0 - 2.0* (y/canvas.height);

    var dDisplay = document.getElementById("deviceCoords");
    dDisplay.innerHTML = "Device Coordinates: (" + x + ", " + y + ")";

    var wDisplay = document.getElementById("worldCoords");
    wDisplay.innerHTML = "World Coordinates: (" + wX + ", " + wY + ")";

    var nDisplay = document.getElementById("normalized");
    nDisplay.innerHTML = "Normalized Device Coordinates (From World): (" + nX + ", " + nY + ")";

    var NDCDisplay = document.getElementById("NDC");
    NDCDisplay.innerHTML = "Normalized Device Coordinates (From Device): (" + ndc_x + ", " + ndc_y + ")";
}
