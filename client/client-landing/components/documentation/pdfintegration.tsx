const PdfFile = () => {
    var sources: string[] = ["https://drive.google.com/file/d/1kPcD_GpBODXD6pUgfLaqPhEHwpB-lpk3/preview", "https://drive.google.com/file/d/1LZzQP5RPTMI4RKzTpnwfA3ufnc60Z2zA/preview"]
    

    return (
        <div>
            <p className="text-3xl my-3">PDF Tutorial</p>
            <div className="content-center  rounded-lg py-2 ">
                {sources.map((source) => (
                    <div className="w-3/5 h-screen my-5 pdfcenter shadow-xl" key={source}>
                        <iframe src={source} height="100%" width="100%" className="rounded-lg"></iframe>
                    </div>
                ))}
            </div>

            this is the end
        </div>)
}

export default PdfFile;