const Hero = () => {
  const domainData: Array<{ img: string; alt: string; text: string }> = [
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ever since the 1500s.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ever since the 1500s.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ever since the 1500s.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ever since the 1500s.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ever since the 1500s.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ever since the 1500s.",
    },
  ];

  return (
    <div>
      <h1 className="flex justify-center text-base-black text-5xl lg:text-7xl font-bold mb-6">
        GitHub SRM
      </h1>

      <div>
        <h2 className="text-4xl font-semibold text-base-black py-4 my-4 text-center">
          OUR FOCUS
        </h2>
      </div>

      <div className="flex flex-col-reverse  lg:flex-row justify-center items-center">
        <p className="text-xl lg:w-8/12 mx-auto py-2 my-2 text-justify items-center">
          Lorem Ipsum is simply dummy text of the printing and typesetting
          industry. Lorem Ipsum has been the industry's standard dummy text ever
          since the 1500s, when an unknown printer took a galley of type and
          scrambled it to make a type specimen book. It has survived not only
          five centuries, but also the leap into electronic typesetting,
          remaining essentially unchanged. It was popularised in the 1960s with
          the release of Letraset sheets containing Lorem Ipsum passages, and
          more recently with desktop publishing software like Aldus PageMaker
          including versions of Lorem Ipsum.
        </p>

        <figure className="w-3/12">
          <img
            src="https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png"
            alt="sample"
            className="w-full"
          />
        </figure>
      </div>

      <div className="flex flex-col justify-center">
        <p className="text-4xl font-semibold text-base-black py-4 my-4 text-center">
          OUR DOMAINS
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-1">
          {domainData.map((data) => (
            <div key={data.img}>
              <div className="flex flex-col justify-center p-6 rounded-xl text-justify">
                <figure className="mx-auto rounded-full overflow-hidden">
                  <img src={data.img} alt={data.alt} />
                </figure>
                <p className="mt-8">{data.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex my-10 items-center flex-col   justify-items-center ">
        <div>
          <div className="p-32 bg-pink-100 mb-10 shadow-xl rounded-xl">abc</div>
          <div className="p-32 bg-pink-100 shadow-xl rounded-xl">abc</div>
        </div>
        <div className="flex flex-col ml-10 items-center justify-center">
          <div className="p-32 bg-pink-100  shadow-xl rounded-xl">abc</div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
