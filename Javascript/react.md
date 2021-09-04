```bash
npm init react-app my-app [--template typescript]
npm start # run in development in http://localhost:3000
npm test #
npm run build # build for production
```

A component takes in parameters `props` and specify the display via `render` function.
```javascript
class MyComponent extends React.Component {
    render() {return (<h1>this.props.value</h1>)}
}

// passing prop `value` to MyComponent
return <MyComponent value={5} />;

const Comp = (props) => {return <div>props.title, props.body</div>}
// equivalent 
const Comp = ({title, body}) => {return <div>title, body</div>}
```