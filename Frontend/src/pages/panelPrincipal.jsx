import Header from "../components/header"
import Buttons from "../components/buttons"
import Grafico from "../components/grafico"

function PanelPrincipal(){

  return(

    <div className="container-fluid p-4">

      <Header/>

      <Buttons/>

      <Grafico/>

    </div>

  )

}

export default PanelPrincipal