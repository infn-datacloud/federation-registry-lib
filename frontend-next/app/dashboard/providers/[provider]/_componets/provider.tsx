import { Suspense } from "react";
import { Provider } from "../../../_lib/dbTypes";
import Loading from "../loading";
import {
  Card,
  CardContent,
  CardHeader,
  Grid,
  List,
  ListItem,
} from "@mui/material";
import Link from "next/link";

export default async function ProviderGrid({
  promise,
}: {
  promise: Promise<Provider>;
}) {
  const provider = await promise;
  return (
    <Suspense fallback={<Loading />}>
      <Grid container spacing={2}>
        <Grid item>
          <Card>
            <CardHeader title="Location" />
            <CardContent>
              <Link href={`/dashboard/location/${provider.location.uid}`}>
                {provider.location.name}
              </Link>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card>
            <CardHeader title="Flavors" />
            <CardContent>
              <List>
                {provider.flavors.map((item, index) => (
                  <Link href={`/dashboard/flavors/${item.uid}`}>
                    <ListItem key={index} disablePadding>
                      {item.name}
                    </ListItem>
                  </Link>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card>
            <CardHeader title="Identity Providers" />
            <CardContent>
              <List>
                {provider.identity_providers.map((item, index) => (
                  <Link href={`/dashboard/identity_providers/${item.uid}`}>
                    <ListItem key={index} disablePadding>
                      {item.endpoint.toString()}
                    </ListItem>
                  </Link>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card>
            <CardHeader title="Images" />
            <CardContent>
              <List>
                {provider.images.map((item, index) => (
                  <Link href={`/dashboard/images/${item.uid}`}>
                    <ListItem key={index} disablePadding>
                      {item.name}
                    </ListItem>
                  </Link>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card>
            <CardHeader title="Projects" />
            <CardContent>
              <List>
                {provider.projects.map((item, index) => (
                  <Link href={`/dashboard/projects/${item.uid}`}>
                    <ListItem key={index} disablePadding>
                      {item.name}
                    </ListItem>
                  </Link>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card>
            <CardHeader title="Services" />
            <CardContent>
              <List>
                {provider.services.map((item, index) => (
                  <Link href={`/dashboard/services/${item.uid}`}>
                    <ListItem key={index} disablePadding>
                      {item.endpoint.toString()}
                    </ListItem>
                  </Link>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Suspense>
  );
}
