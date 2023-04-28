import React from 'react';
import jsPDF from 'jspdf';
class Drop extends React.Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();

    this.state = {
      tab: '',
      fetchedData: null, // initialize the fetchedData
      fileName: '',
      pdfTitle: '',
      options: [], selectedValue: '' 
    };

    this.handleUpload = this.handleUpload.bind(this);
    this.handleTitleChange = this.handleTitleChange.bind(this);
    this.handleSelectChange = this.handleSelectChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
  }
  
  handleTitleChange(event) {
    this.setState({ pdfTitle: event.target.value });
  }

  handleUpload(event) {
    event.preventDefault();
    

    const data = new FormData();
    const uploadedFile = this.fileInput.current.files[0];
    data.append('file', uploadedFile);
    this.setState({ fileName: uploadedFile.name.split('.')[0] }); // set the file name

    fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.log(body);
        this.setState({ fetchedData: body }); // set the state with the data from /upload
      });
    });
    document.getElementById("pdfTitle").value = ""
    document.getElementById("SavePDF").disabled = false
    
  }
  handleClick = async () => {
    const response = await fetch('/getTuning');
    const tuningList = await response.json();
    const dropdown = document.getElementById('tuningDropdown');
    dropdown.innerHTML = '';
    console.log(tuningList)
    tuningList.forEach((tuning) => {
      const option = document.createElement('option');
      option.value = tuning;
      option.text = tuning;
      dropdown.appendChild(option);
    });
  };

  handleSelectChange(event) {
    
    this.setState({ selectedValue: event.target.value });
  }
  generatePDF() {
    const { fetchedData, fileName, pdfTitle } = this.state;
    document.getElementById("SavePDF").disabled = true
    const pdfContent = fetchedData.tab;
    const pdf = new jsPDF();
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
  
    // Set font to monospace (courier)
    pdf.setFont('courier');
  
    // Add title and center it
    pdf.setFontSize(14);
    const titleWidth = pdf.getStringUnitWidth(pdfTitle) * pdf.getFontSize() / pdf.internal.scaleFactor;
    const titleXPosition = (pageWidth - titleWidth) / 2;
    pdf.text(pdfTitle, titleXPosition, 20);
  
    // Add content below the title
    pdf.setFontSize(10);
    const scores = pdfContent.split('\n\n');
    let yPosition = 30;
    let xPosition = 10;
    let column = 0;
  
    scores.forEach((score) => {
      const scoreLines = score.split('\n');
      const maxLineWidth = Math.max(...scoreLines.map(line => pdf.getStringUnitWidth(line) * pdf.getFontSize() / pdf.internal.scaleFactor));
      const scoreWidth = maxLineWidth;
  
      if (column === 1 && xPosition + scoreWidth > pageWidth - 10) {
        column = 0;
        yPosition += 30;
        xPosition = 10;
      }
  
      if (yPosition + 30 > pageHeight - 10) {
        pdf.addPage();
        yPosition = 30; // Reset the yPosition for the new page
      }
  
      pdf.text(score, xPosition, yPosition);
  
      if (column === 0 && xPosition + scoreWidth <= pageWidth / 2) {
        column += 1;
        xPosition = pageWidth / 2;
      } else {
        column = 0;
        yPosition += 30;
        xPosition = 10;
      }
    });
  
    pdf.save(`${fileName}.pdf`);
    
  }
  handleTuningChange = (event) => {
    event.preventDefault();
    const data = new FormData();
    const uploadedFile = this.fileInput.current.files[0];
    console.log(uploadedFile.name)
    //data.append('file', uploadedFile);
    //this.setState({ fileName: uploadedFile.name.split('.')[0] }); // set the file name
    const selectedTuning = this.state.selectedValue;
    fetch(`/changeTuning/${selectedTuning}/${uploadedFile.name}`, {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.log(body);
        this.setState({ fetchedData: body }); // set the state with the data from /upload
      });
    });
    
  };


  render() {
    const { fetchedData } = this.state;
    return (
      <body>
        
        <div id="upload">
          <h1>Choose a file to upload</h1>
          <form id="choose file" onSubmit={this.handleUpload}>
            <div>
              <input ref={this.fileInput}  type="file" onChange={this.handleFileInputChange} />
            </div>
            <br />
            <div>
              <button className="button-19" id="Upload">Upload</button>
            </div>
          </form>
          {/* Display fetched data */}
          {fetchedData ? (
            
            <div className="tab">
              {/* Title input */}
              <label htmlFor="pdfTitle">PDF Title:</label>
              <input
                type="text"
                id="pdfTitle"
                name="pdfTitle"
                onChange={this.handleTitleChange}
              />
              {/* Save as PDF button */}
              <button id="SavePDF" onClick={() => this.generatePDF()}>Save as PDF</button>

              <select id='tuningDropdown' value={this.state.selectedValue} onChange={this.handleSelectChange}>
              {this.options}
              </select>
              <p>Selected tuning: {this.state.selectedValue}</p>
              <button id="generateTuningsBtn" onClick={this.handleClick}>Generate Tunings</button>
              <button id="changeTuning" onClick={this.handleTuningChange}>Submit</button>
                {/* Display JSON data */}
                  <p className="pdf-content">
                    {fetchedData.tab}
                  </p>
            </div>
          ) : null}
          
          <div>
          

      </div>

        </div>
      </body>
    );
  }
}

export default Drop;