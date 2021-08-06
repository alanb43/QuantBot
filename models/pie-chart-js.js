class PChartElement extends HTMLElement {
    connectedCallback() {
    }
}

class PChart extends HTMLElement {
    shorten_text = function (text, max_chars) {
        var return_val = ""
        if (text.length > max_chars) {
            return text.substr(0,max_chars) + "...";
        } else {
            return text
        }
    }

    totalFunc = function (total, num) {
        return total + num;
    }  

    getPoint = function (c1,c2,radius,angle){
        return [c1+Math.cos(angle)*radius,c2+Math.sin(angle)*radius];
    }
    getAngle = function(x_coord,y_coord,x_origin,y_origin) {
        var radius = Math.sqrt(Math.pow(Math.abs(x_coord-x_origin),2) + Math.pow(Math.abs(y_coord-y_origin),2));
        if (Math.acos(Math.abs(x_coord-x_origin)/radius).toFixed(6) == Math.asin(Math.abs(y_coord-y_origin)/radius).toFixed(6) && radius <=this.radius)
        {
            var theta = Math.acos(Math.abs(x_coord-x_origin)/radius);
            if (x_coord - x_origin > 0 && y_coord - y_origin < 0) {
                return (2 * Math.PI) - theta;
            }
            if (x_coord - x_origin < 0 && y_coord - y_origin < 0) {
                return (Math.PI) + theta;
            }
            if (x_coord - x_origin < 0 && y_coord - y_origin > 0) {
                return (Math.PI) - theta;
            }
            if (x_coord - x_origin > 0 && y_coord - y_origin > 0) {
                return theta;
            }
        } else {
            return null;
        }
    }
    drawChart = function() {
        this.arcs = [] 
        var elements = this.getElementsByTagName("pchart-element");
        this.names = [];
        this.vals = [];
        this.colours = [];
        for (i = 0; i < elements.length; i++)
        {
            this.names.push(elements[i].getAttribute("name"));
            this.vals.push(parseFloat(elements[i].getAttribute("value")));
            this.colours.push(elements[i].getAttribute("colour"))
        }
        var shadow = this.shadowRoot;
        var c = this.shadowRoot.querySelector("canvas");
        var positionInfo = this.getBoundingClientRect();
        var height = positionInfo.height;
        var width = positionInfo.width;
        c.width  = width;
        c.height = height;
        var ctx = c.getContext("2d");

        var font_size = parseInt(width * 0.02166847);

        var max_font_size = 28;

        if (font_size > max_font_size) {
            font_size = max_font_size;
        }


        this.y_origin = height * 0.5;
        this.x_origin = c.width * 0.5;
        this.radius = c.width * 0.35;
        var max_radius = c.height * 0.35;
        if (this.radius > max_radius) {
            this.radius = max_radius;
        }

        var share_percentage = [];

        var x = c.width - parseInt(c.width * 0.12019231) * 1.25;
        var y = font_size;

        ctx.beginPath();
        var rect_height = (this.names.length * font_size) + 20;
        ctx.rect(x, y+10, parseInt(c.width * 0.12019231), rect_height);
        ctx.stroke();
        y += 10;
        for (var i=0;i<this.names.length;i++)
        {
            var percentage = this.vals[i] / this.vals.reduce(this.totalFunc);
            share_percentage.push(percentage);

            y += font_size;
            ctx.beginPath();
            ctx.fillStyle = this.colours[i];
            ctx.fillRect(x + 5, y-font_size/2, 5, 5);

            ctx.font = String(font_size) + "px Arial";
            var shorten = 0;
            if (ctx.measureText(this.names[i]).width > parseInt(c.width * 0.12019231)-15) {
                while(ctx.measureText(this.shorten_text(this.names[i],this.names[i].length - shorten)).width > (parseInt(c.width * 0.12019231)-15) && this.names[i].length - shorten>0) {
                    shorten++;
                }
            }
            ctx.fillText(this.shorten_text(this.names[i],this.names[i].length - shorten), x + 15, y);
            ctx.closePath();
        }
        for (var i = 0; i < share_percentage.length; i++)
        {
            if (i == 0)
            {
                start = 0;
            } else {
                var start = share_percentage.slice(0,i).reduce(this.totalFunc);
            }
            var end = (start + share_percentage[i]);
            ctx.beginPath();
            ctx.arc(this.x_origin, this.y_origin, this.radius, start * 2 * Math.PI, end * 2 * Math.PI);
            var arc_start = this.getPoint(this.x_origin,this.y_origin,this.radius,start * 2 * Math.PI);
            var arc_end = this.getPoint(this.x_origin,this.y_origin,this.radius,end * 2 * Math.PI);
            this.arcs.push([start * 2 * Math.PI, end * 2 * Math.PI]);
            var arc_middle = this.getPoint(this.x_origin,this.y_origin,this.radius+10,((start + end)) * Math.PI);
            ctx.lineTo(this.x_origin,this.y_origin);
            ctx.lineTo(arc_start[0],arc_start[1]);
            ctx.fillStyle = this.colours[i];
            ctx.fill();
            ctx.fillStyle = this.colours[i];
            if (arc_middle[0].toFixed(2) < this.x_origin)
            {
                ctx.textAlign = "end";
            } else {
                if (arc_middle[0].toFixed(2) == this.x_origin)
                {
                    ctx.textAlign = "center";
                } else {
                    ctx.textAlign = "start";
                }
            }
            if (arc_middle[1] > this.y_origin)
            {
                arc_middle = this.getPoint(this.x_origin,this.y_origin,this.radius+25,((start + end)) * Math.PI);
            }
            ctx.moveTo(arc_middle[0],arc_middle[1]);
            ctx.fillText(this.vals[i].toFixed(2), arc_middle[0], arc_middle[1]);
            ctx.closePath();
        }
    }
    resize = function() {
        var c = this.shadowRoot.querySelector("canvas");
        var positionInfo = this.getBoundingClientRect();
        var height = positionInfo.height;
        var width = positionInfo.width;
        c.width  = width;
        c.height = height;
        this.drawChart();
    }
    getPos = function(e){
        var mouse_x = e.clientX - this.getBoundingClientRect().left;
        var mouse_y = e.clientY - this.getBoundingClientRect().top;
        var mouse_angle = this.getAngle(mouse_x,mouse_y,this.x_origin, this.y_origin);
        if (mouse_angle != null)
        {
            //console.log(mouse_angle);
            //console.log(this.arcs);
            for (var i = 0; i < this.arcs.length; i++)
            {
                if (mouse_angle > this.arcs[i][0] && mouse_angle < this.arcs[i][1])
                {
                    if (!this.shadowRoot.querySelector("#Mouse_Point_Div"))
                    {
                        var c = this.shadowRoot.querySelector("canvas");
                        var ctx = c.getContext("2d");
                        var div = document.createElement("div");
                        div.setAttribute("id","Mouse_Point_Div");
                        div.style.position = "absolute";
                        div.style.left = "0px";
                        div.style.top = "0px";
                        div.style.padding = "5px";
                        //div.style.height = "20px";
                        div.style.backgroundColor = "white";
                        div.style.border = "thin";
                        div.style.borderColor = "black";
                        div.style.borderStyle = "solid";
                        div.style.boxShadow = "4px 4px 2px -2px rgba(0,0,0,0.9)";
                        //div.style.outline = "solid";
                        //div.style.outlineColor = "black"
                        div.style.color = "black";
                        this.shadowRoot.appendChild(div);
                    } else {
                        var div = this.shadowRoot.querySelector("#Mouse_Point_Div");
                        div.style.display = "block";
                        div.innerHTML = "Title: " + this.names[i] + "<br>" + "Value: " + this.vals[i];
                        div.style.left = mouse_x + 'px';
                        div.style.top = mouse_y + 'px';
                        //console.log("Divider Position:", div.style.left);
                    }
                    //console.log(mouse_x + 'px');
                    //div.style.left = mouse_x + 'px';
                    //div.style.right = mouse_y + 'px';
                    //console.log(this.names[i]);
                }
            }
            //console.log(this.names[this.arcs.indexOf(closest)]);
        } else {
            if (this.shadowRoot.querySelector("#Mouse_Point_Div"))
            {
                var div = this.shadowRoot.querySelector("#Mouse_Point_Div");
                div.style.display = "none"
            }
        }
    }
    mouseOver = function(e){
        this.mouse_track = true;
    }
    mouseLeave = function(e) {
        this.mouse_track = false;
    }
    connectedCallback() {
        var shadow = this.attachShadow({mode: 'open'});
        var c = document.createElement('canvas');
        shadow.appendChild(c);
        this.drawChart();
        this.addEventListener("mouseover",this.mouseOver);
        this.addEventListener("mouseleave",this.mouseLeave);
        this.addEventListener("mousemove",this.getPos);
        this.mouse_track = false;
    }
}

//var pchart_element = Object.create(HTMLElement.prototype);
window.customElements.define('pchart-element',PChartElement);
window.customElements.define('pie-chart',PChart);