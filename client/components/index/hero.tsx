const Hero = () => {
  return (
    <>
      <div className="grid grid-cols-2 h-96 text-center">
        <div className="bg-black text-white">
          <div className="flex items-center justify-end h-full mr-40 text-2xl">
            <h1>Testimonials</h1>
          </div>
        </div>
        <div className="grid grid-row-2">
          <div className="bg-black text-white flex justify-center items-center px-10">
            <div>
              <h3>LINDA HUDSON</h3>
              <p>
                "Aenean pulvinar dui ornare, feugiat lorem non, ultrices justo.
                Mauris efficitur, mauris in auctor euismod, quam elit ultrices
                urna"
              </p>
            </div>
            <div>
              <img
                src="https://asia.olympus-imaging.com/content/000107507.jpg"
                alt="bird"
                className="rounded-full"
              />
            </div>
          </div>
          <div className="bg-black text-white flex justify-center items-center px-10">
            <div>
              <h3>LINDA HUDSON</h3>
              <p>
                "Aenean pulvinar dui ornare, feugiat lorem non, ultrices justo.
                Mauris efficitur, mauris in auctor euismod, quam elit ultrices
                urna"
              </p>
            </div>
            <div>
              <img
                src="https://asia.olympus-imaging.com/content/000107507.jpg"
                alt="bird"
                className="rounded-full"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 mt-20 w-11/12 mx-auto">
        <div className="flex justify-center item-centers bg-yellow-500">
          <img
            src="https://asia.olympus-imaging.com/content/000107507.jpg"
            alt="birdy"
          />
        </div>

        <div className="justify-items-center bg-red-500">Thiss</div>
      </div>
    </>
  );
};

export default Hero;
