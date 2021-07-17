import Head from "next/head";

import { Layout } from "../components/shared";
import { ContactUs } from "../components/contact-us";

const ContactPage = () => {
  return (
    <>
      <Head>
        <title>GitHub Community SRM | Contact Us</title>
        <meta
          name="description"
          content="GitHub Community SRM is the foremost student-led community spearheading open-source revolution in SRMIST."
        />
      </Head>
      <Layout>
        <ContactUs />
      </Layout>
    </>
  );
};

export default ContactPage;
