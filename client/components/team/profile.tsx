import Socials from "./socials";

interface member {
  Name: string;
  GitHub_ID: string;
  LinkedIn: string;
  Twitter: string;
  Portfolio: string;
  Img_URL: string;
  Tagline: string;
}

const Profile = () => {
  const users: member[] = [
    {
      Name: "Abhishek Saxena",
      GitHub_ID: "URL",
      LinkedIn: "URL2",
      Twitter: "URL3",
      Portfolio: "URL4",
      Img_URL: "./test.webp",
      Tagline: "Bullshit",
    },
    {
      Name: " Yashwardhan Jagnani",
      GitHub_ID: "URL",
      LinkedIn: "URL2",
      Twitter: "URL3",
      Portfolio: "URL4",
      Img_URL: "./test2.webp",
      Tagline: "less Bullshit",
    },
  ];
  return (
    <div className="flex flex-wrap">
      {users.map((user) => (
        <div className="flex flex-col items-center m-4">
          <img
            className="rounded-full w-48 h-48 object-cover"
            src={user.Img_URL}
          ></img>
          <div className="text-lg font-montserrat font-normal">{user.Name}</div>
          <div className="text-lg font-montserrat font-extralight">
            {"'" + user.Tagline + "'"}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Profile;
