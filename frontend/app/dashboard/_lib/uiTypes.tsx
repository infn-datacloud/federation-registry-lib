import { Url } from "next/dist/shared/lib/router/router";

export type SideBarItem = {
  title: string;
  icon: React.ReactNode;
  link: Url;
};

