
function create_table() {
    var x = "", i, j;
    x += '<table>';
    x += '<th>Topics by Category</th>';
    
    for (i=0; i<topics.length; i++) {
        x = x + '<tr><td><h2 style="margin: 5px"id="' + topics[i] + '">' + topics[i] +'</h2>';
        for (j =0; j<search_terms[i].length; j++){
            x = x + '<div style="padding: 0px; display: inline; line-height: 28px">';
            x = x + ' <div class="dropdown"><button class="dropbtn"> ' + search_terms[i][j] + ' </button><div class="dropdown-content"><a  href="https://digitalricoeur.org/;((%22c%22%20.%20%220n0EExs8u8tfeWjfL2iS3XUClxSooKDMpIDMgKCgobGliICJ3ZWItc2VydmVyL2xhbmcvYWJvcnQtcmVzdW1lLnJrdCIpIC4gImxpZnRlZC4zIikgKChsaWIgIndlYi1zZXJ2ZXIvbGFuZy93ZWItY2VsbHMucmt0IikgLiBkZXNlcmlhbGl6ZS1pbmZvOmZyYW1lLXYwKSAoKGxpYiAicmljb2V1ci9wb3J0YWwvdGVybS1zZWFyY2gucmt0IikgLiAibGlmdGVkLjE0NSIpKSAwICgpICgpICgwICgxIChoIC0gKCkgKGxpZnRlZC41NC0wIC4gIi8iKSAobGlmdGVkLjI0NDAtOCAuICNmKSAobGlmdGVkLjI0MDQtNiAuICN0KSAobGlmdGVkLjEyMDA2LTIgLiBsYXRlc3QtdG8tb2xkZXN0KSAobGlmdGVkLjEyMDI0LTMgLiBsYXRlc3QtdG8tb2xkZXN0KSAobGlmdGVkLjE1ODUtNCAuIHRlbXAxNSkgKGxpZnRlZC4yMzg2LTUgLiBmaXJzdC0+bGFzdCkgKGxpZnRlZC4yNDU4LTkgLiBhbnkpIChsaWZ0ZWQuMjQyMi03IC4gI3QpIChsaWZ0ZWQuMTE5ODgtMSAuIGxhc3QtdXNlZCkgKGxpZnRlZC4xMDM4LTEwIC4gdGVtcDEpKSkgKGMgKHYhICgyKSAjZiAjZikpKSk=%22))?input_0=' + search_terms[i][j] +'">Primary Source</a><a  href="../Python-Ricoeur-JstoreSearcher/Digital-Ricoeur-Jstor-' + search_terms[i][j] + '.html">Secondary Source</a></div></div>';
        }
        // x = x + '</div></td><td><button onclick="topFunction()" title="Go to top">&#8679; Top</button></td></tr> ';
    }
    x += '</table>';
    document.getElementById("sections").innerHTML = x;
}

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        document.getElementById("toTop").style.display = "block";
    } else {
        document.getElementById("toTop").style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}


var topics = ["History","Evil","Testimony","Choice","Language","Memory","Concept","Par","Critique","Language","Phenomenology","Death","Language","Ideology","Man","Body","Substance","Discourse","Psychoanalysis","Ideology","Pleasure","Pp","Project","Meaning","Conscience","Emotion","Action","Freedom","Image","Utopia","Man","Dream","Text","Gt","Metaphor","Freedom","Justice","Logic","Text","Time"];
var search_terms = [
                    ["history","philosophy","truth","work","time","explanation","event"],
                    ["evil","myth","sin","man","theology","world","experience"],
                    ["testimony","freedom","meaning","witness","hope","consciousness","time"],
                    ["choice","attention","freedom","act","project","consciousness","decision"],
                    ["language","text","translation","work","time","word","meaning"],
                    ["memory","die","time","history","representation","past","work"],
                    ["concept","labor","ideology","alienation","production","man","relation"],
                    ["par","consciousness","world","cf","meaning","reduction","phenomenology",],
                    ["critique","experience","text","interpretation","understanding","tradition","ideology"],
                    ["language","philosophy","time","history","work","problem","relation"],
                    ["phenomenology","sense","consciousness","ego","world","experience","body"],
                    ["death","time","life","work","memory","narrator","relation"],
                    ["language","theory","philosophy","system","science","problem","question"],
                    ["ideology","critique","action","situation","psychoanalysis","process","concept"],
                    ["man","history","power","work","world","violence","word"],
                    ["body","action","movement","effort","object","world","consciousness"],
                    ["substance","philosophy","problem","soul","science","form","question"],
                    ["discourse","text","meaning","world","work","language","reference"],
                    ["psychoanalysis","theory","meaning","work","language","interpretation","point"],
                    ["ideology","concept","order","system","relation","function","action"],
                    ["pleasure","pain","life","imagination","object","body","feeling"],
                    ["pp","translation","cit","der","op","philosophy","du"],
                    ["project","decision","consciousness","action","description","relation","possibility"],
                    ["meaning","interpretation","symbol","reflection","language","symbolism","consciousness"],
                    ["conscience","sense","logic","question","gift","rule","justice"],
                    ["emotion","habit","body","consciousness","desire","movement","action"],
                    ["action","sense","question","identity","character","relation","person"],
                    ["freedom","death","consciousness","consent","necessity","man","experience"],
                    ["image","world","fiction","imagination","sense","meaning","language"],
                    ["utopia","language","sense","imagination","action","ideology","world"],
                    ["man","reflection","thing","point","idea","synthesis","finitude"],
                    ["dream","work","philosophy","experience","point","interpretation","man"],
                    ["text","discourse","revelation","sense","world","language","faith"],
                    ["gt","lt","ego","principle","reality","death","desire"],
                    ["metaphor","level","meaning","language","word","discourse","sense"],
                    ["freedom","consciousness","life","character","necessity","man","nature"],
                    ["justice","idea","law","sense","state","fact","order"],
                    ["logic","theory","philosophy","language","law","science","reality"],
                    ["text","interpretation","language","explanation","discourse","world","relation"],
                    ["time","work","text","story","reader","history","fiction"]
                    ];
