import Left from "./left";
import Right from "./right";

const Contact = () => {
  return (
    <div className="flex flex-col lg:flex-row">
      <div className="w-1/2">
        <Left />
      </div>
      <div className="w-1/2">
        <Right />
      </div>
    </div>
  );
};

export default Contact;
