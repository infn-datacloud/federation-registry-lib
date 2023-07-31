import { Card, CardContent, CardHeader, Typography } from "@mui/material";
import { UserGroup } from "../_lib/dbTypes";

export default function UserGroupCard({ item }: { item: UserGroup }) {
  return (
    <Card>
      <CardHeader title="User Group" />
      <CardContent>
        <Typography>Name: {item.name}</Typography>
        <Typography>
          IDP URL: {item.identity_provider?.endpoint.toString()}
        </Typography>
      </CardContent>
    </Card>
  );
}
