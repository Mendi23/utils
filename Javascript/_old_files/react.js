// function component (rcf<e>)
const Comp = (props) => {
    // returning fragment, no enclosing parent tag <></>
    return (<>JSX</>)
}

export default Comp

Comp.defaultProps = {
    title: 'default value'
}

// PropTypes (impt)
import PropTypes from 'prop-types'
Comp.propTypes = {
    title: PropTypes.string,
    head: PropTypes.string.isRequired
}


// styling
const compStyle = {
    color: 'red',
    backgroudColor: 'black'
} // inside JSX: <div style={compStyle}>
// class = className