interface OSSProps {
  title: string;
}

export default function OSS({ title }: OSSProps) {
  return (
    <svg
      className=""
      viewBox="0 10 1066 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <text
        fill="url(#paint0_linear)"
        xmlSpace="preserve"
        style={{ whiteSpace: "pre" }}
        fontFamily="Montserrat"
        fontSize="400"
        letterSpacing="0em"
      >
        <tspan x="-1.757812" y="300.4">
          {title}
        </tspan>
      </text>
      <defs>
        <linearGradient
          id="paint0_linear"
          x1="551"
          y1="-107"
          x2="551"
          y2="490.348"
          gradientUnits="userSpaceOnUse"
        >
          <stop stopColor="#284B63" />
          <stop offset="0.75" stopColor="white" stopOpacity="0" />
        </linearGradient>
      </defs>
    </svg>
  );
}
