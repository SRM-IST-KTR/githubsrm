import { Layout } from "../components/shared";
import { ContactUs } from "../components/contact-us";
import Head from "next/head";

const ContactPage = () => {
  return (
    <div>
      <Head>
        <title>GitHub Community SRM | Contact</title>
        <meta
          name="description"
          content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
        />
      </Head>
      <Layout>
        <ContactUs />
      </Layout>
    </div>
  );
};

export default ContactPage;
