import { UserGroup } from "@/app/dashboard/_lib/dbTypes";
import { Card, CardContent, CardHeader, Typography } from "@mui/material";

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
