var badIDList = [];

function deltaBorder(obj) {
    if(obj.style.opacity!=0.5) {
        obj.style.filter='alpha(opacity=50)';
        obj.style.opacity=0.5;
        badIDList.push(obj.id);
    }
    else {
        obj.style.filter='alpha(opacity=0)';
        obj.style.opacity=1.0;
        badIDList.splice(badIDList.indexOf(obj.id), 1);
    }
    console.log(badIDList);
}

function getData(obj) {
    obj.value = JSON.stringify(badIDList);
}

