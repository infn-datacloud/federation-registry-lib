import { Suspense } from "react";
import Loading from "./loading";
import Card from "@mui/material/Card";
import { CardContent, CardHeader, Typography } from "@mui/material";

async function getProviders() {
  const res = await fetch("http://localhost:8000/providers/", {
    cache: "no-store",
  });
  if (res.status != 200) {
    throw new Error("Failed to fetch data");
  }
  return res.json();
}

export default async function Page() {
  const providers = await getProviders();
  return (
    <>
      <Suspense fallback={<Loading />}>
        <Providers promise={providers} />
      </Suspense>
    </>
  );
}

async function Providers({ promise }: { promise: Promise<Provider[]> }) {
  const providers = await promise;
  return (
    <ul>
      {providers.map((provider) => (
        <Card key={provider.name}>
          <CardHeader title={provider.name} />
          <CardContent>
            <Typography>
              {provider.is_public ? "Public" : "Private"} provider
            </Typography>
            <Typography>Country: {provider.location.country}</Typography>
            <Typography>
              Support Emails: {provider.support_emails.join(", ")}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </ul>
  );
}

type Provider = {
  name: string;
  is_public: boolean;
  support_emails: string[];
  location: Location;
};

type Location = {
  name: string;
  country: string;
  latitude?: number;
  longitude?: number;
};
