import Head from "next/head";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import "../styles/tailwind.styles.css";

function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>GitHub Community SRM</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <span className="purge-prevention hidden" />
      <ToastContainer />
      <Component {...pageProps} />
    </>
  );
}

export default MyApp;
