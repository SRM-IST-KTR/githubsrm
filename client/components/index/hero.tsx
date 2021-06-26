import { motion, useViewportScroll, useTransform } from "framer-motion";

interface HeroProps {
  reference?: HTMLDivElement;
}

const Hero = ({ reference }: HeroProps) => {
  const domainData: Array<{
    img: string;
    alt: string;
    text: string;
  }> = [
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Students can contribute to Open Source Projects under the banner of SRMIST allowing students to get industry-level exposure through SRMIST’s organization.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",

      text: "It also helps us maintain a record of all the contributions students have made under the banner of SRMIST.      ",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",

      text: "Travis CI Enterprise license. Travis CI is a continuous integration platform, allowing to run CI/CD pipelines where builds, unit tests, and integration tests can be executed.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "A GitHub Education Swag Bag for your students every semester.",
    },

    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "Inculcates healthy competition within students encouraging them to contribute further to industry-level projects present in the open-source domain under the banner of SRMIST.",
    },
    {
      img: "https://img.stackshare.io/service/10608/default_2e4e6445d2b6326eb7c7748f17ae5109a99121fc.png",
      alt: "logo",
      text: "This initiative can lead to major project development/contributions to large organizations under the banner of SRMIST.",
    },
  ];

  const { scrollYProgress } = useViewportScroll();
  const y = useTransform(scrollYProgress, [0, 0.15], [1, 0]);

  return (
    <div>
      <motion.h1
        style={{ y: y }}
        className="flex justify-center text-base-black text-5xl lg:text-7xl font-bold mb-6"
      >
        GitHub SRM
      </motion.h1>

      <div className="flex flex-col-reverse  lg:flex-row justify-center items-center">
        <div className="text-xl lg:w-8/12 mx-auto py-2 my-2 text-justify items-center">
          <p>
            GitHub Community SRM is the official/foremost student-led community
            spearheading the Open Source Revolution at SRMIST, Chennai.
          </p>
          <br />
          <p>
            We have successfully brought the GitHub Campus Partner Program to
            SRMIST, enabling all SRMIST students to apply for the Github
            Externship Program. In addition, the program has given SRMIST access
            to Premium Enterprise licensing to GitHub, Travis, and GitKraken
            accounts.
          </p>
          <br />
          <p>
            We plan on administering the SRMIST KTR GitHub Enterprise
            organization, helping the faculties in managing student projects,
            and helping the students get onboarded and get started with their
            projects.
          </p>
        </div>

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
          Benefits of being a GitHub Campus Partner Program
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-1">
          {domainData.map((data) => (
            <div key={data.img}>
              <div className="flex flex-col justify-center p-6 rounded-xl text-justify">
                <figure className="mx-auto rounded-full overflow-hidden">
                  <img src={data.img} alt={data.alt} />
                </figure>

                <p className="text-md mt-5">{data.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="hidden lg:block">
        <div className="flex flex-col justify-items-center my-20  items-center">
          <div className="flex my-10  justify-items-center ">
            <div>
              <div className="px-32 py-48 bg-gray-100 mb-5 shadow-xl rounded-xl">
                abc
              </div>
            </div>
            <div className="flex flex-col ml-5 ">
              <div className="py-32 px-44 mb-5 bg-gray-100 shadow-xl rounded-xl">
                abc
              </div>
              <div className="w-3/4 py-20 text-center bg-gray-100  shadow-xl rounded-xl">
                abc
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
