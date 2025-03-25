// Full spec: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions

// defining regex
var regex = new RegExp(/name:(\w+)/, 'g')
var regex = /name:(\w+)/g
var regex = new RegExp("name:(\\w+)", 'g') // notice escaping characters when constructing from a string
s = "name:(\\w+)"; var regex = new RegExp(s, 'g') // ''

/* s.matchAll is newly introduced */ Array.from(s.matchAll(regex), m => m[0]); // multiple matches, get captured groups
Array.from(func_to_iter(()=>regex.exec(s)), (m)=>m[1]); // get just captured groups (one group)
