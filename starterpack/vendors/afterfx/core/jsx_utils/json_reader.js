#include "json2.js";

function readJsonFile(filepath) {
    var file = File(filepath);
    file.open("r");
    var content = file.read();
    file.close();
    return JSON.parse(content);
}

function readJsonString(string) {
    return JSON.parse(string);
}