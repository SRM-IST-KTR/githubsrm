import Head from 'next/head';

import { Layout } from '../components/shared/index';
import FaqComponent from '../components/faq/faq';

const Faq = () => {
  return (
    <>
      <Head>
        <title>FAQ</title>
        <meta
          name='description'
          content='A team of 11 students of SRMIST trying to spearhead open-source revolution in SRMIST through the GitHub Community SRM'
        />
      </Head>
      <Layout>
        <FaqComponent />
      </Layout>
    </>
  );
};

export default Faq;
