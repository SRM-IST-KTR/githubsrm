import Head from "next/head";

import "../styles/tailwind.styles.css";

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>GitHub Community SRM</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
