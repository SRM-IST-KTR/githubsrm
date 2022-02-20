interface linkProps {
  source: {
    href: string;
    title?: string;
    subTitle?: string;
    content?: string;
    name?: string;
    icon?: JSX.Element;
  };
}

const YoutubeDisplay = ({ source }: linkProps) => {
  return <>{source.href}</>;
};

export default YoutubeDisplay;
