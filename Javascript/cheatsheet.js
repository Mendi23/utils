
const a = Array(5);
const { a, b } = t; // a = t.a; b = t.b;

// -- special functions


// --- generators
yield *a // yield from <expression>
function *generator() {} // defining generator function


// --- ellipsis (...)
function f (a, ...b) {} // like *args (gathering)
f(...a) // like *a (expanding)
const l1 = [1,2]; const l2 = [3,4]; const l3 = [...l1, ...l2, 5]; // l3 = [1,2,3,4,5]
const d1 = {'a':1}; const d2 = {'a':2, 'b':3}; const d3 = {...d2, ...d1}; // d3 = {'a':1, 'b':3}
const arr = [...generator()] // expands generator and iterator


// --- classes
let UnnamedClass = class {
  constructor() {}
};

class MyClass extends UnnamedClass {
    public_field = 7;
    #private_field;
  constructor(a) {
      super()
      this.a = a
      this.#private_field = 5
  }
  get attribute () { // getter
      return this.a
  }
  *generator_function() {
      yield* Array(this.public_field).keys()
  }
  };
  const p = new MyClass(9);
  console.log(p.name); // MyClass
  console.log(p.attribute); // 9 (p.a)

// url
const url = new URL('https://www.yad2.co.il/')
url.search = new URLSearchParams({'param1': 1, 'param2': 2}) // setting all params
url.searchParams.set('param1', 'value') // setting one param
url.toString()