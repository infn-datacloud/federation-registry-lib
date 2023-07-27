import { Location } from "../../../locations/_lib/types";

export type Provider = {
  uid: string;
  name: string;
  is_public: boolean;
  support_emails: string[];
  location: Location;
};
