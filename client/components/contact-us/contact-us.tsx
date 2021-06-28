import { Socials, Form } from "./";

const ContactUs = () => {
  return (
    <div className="flex flex-col lg:flex-row">
      <div className="w-1/2">
        <Socials />
      </div>
      <div className="w-1/2">
        <Form />
      </div>
    </div>
  );
};

export default ContactUs;
