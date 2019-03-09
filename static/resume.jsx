class Resume extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      "name": "",
      "title": ""
    }
  }
  
  componentDidMount() {
    let route = '/resume.json';
    $.get(route, results => {
      console.log(results)

      this.setState({
        name: results.name,
        title: results.title
      });
    });


    
  }

  render() {
    return(

      <div className="container-fluid">
      
      <br>
      <h4> { this.state.name }, { this.state.title }</h4>
      Hackbright Academy, March 2019 Grad
      
      <br>
      <br>

      <h5> ProTag's Inspiration</h5>
      Ryan's love for hip hop and data inspired her to create ProTag.  She grew
      up listening to 90s West Coast rap and considers this an ode her 14 year old
      self, who was often punished growing up for rapping the explicit lyrics of 
      her favorite rap songs.  
      
      </div>
    );
  }
}

const successRes = document.getElementById('resume');

ReactDOM.render(
  <Resume isNewUser={successRes.dataset.isNewUser}/>,
  document.getElementById('resume')
);