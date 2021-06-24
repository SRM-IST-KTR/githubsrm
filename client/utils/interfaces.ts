export interface MemberProps {
  name: string;
  gitHub_id: string;
  handles?: { [handle: string]: string }[];
  img_url: string;
  tagline: string;
}
