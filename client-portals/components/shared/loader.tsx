import Loader from "react-loader-spinner";

const CSSLoader = () => {
  return (
    <Loader
      type="Puff"
      color="#79BA6E"
      height={100}
      width={100}
      timeout={3000} //3 secs
    />
  );
};
export default CSSLoader;
