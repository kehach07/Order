<script lang="ts">
  import {
    CreditCard,
    Calendar,
    AlertCircle,
    CheckCircle,
    Clock
  } from "lucide-svelte";

  import Card from "$lib/components/ui/Card.svelte";
  import CardHeader from "$lib/components/ui/CardHeader.svelte";
  import CardContent from "$lib/components/ui/CardContent.svelte";
  import CardTitle from "$lib/components/ui/CardTitle.svelte";
  import CardDescription from "$lib/components/ui/CardDescription.svelte";
  import Button from "$lib/components/ui/Button.svelte";
  import Badge from "$lib/components/ui/Badge.svelte";
  import Progress from "$lib/components/ui/Progress.svelte";

  const upcomingPayments = [
    { id: "PAY-001", orderId: "ORD-2024-001", client: "ABC Corporation", amount: "₹25,000", dueDate: "Jan 15, 2025", daysLeft: 5, status: "upcoming" },
    { id: "PAY-002", orderId: "ORD-2024-002", client: "XYZ Industries", amount: "₹15,200", dueDate: "Jan 18, 2025", daysLeft: 8, status: "upcoming" },
    { id: "PAY-003", orderId: "ORD-2024-004", client: "Global Trade Co", amount: "₹8,900", dueDate: "Jan 12, 2025", daysLeft: 2, status: "urgent" },
    { id: "PAY-004", orderId: "ORD-2024-006", client: "Metro Distributors", amount: "₹32,400", dueDate: "Jan 25, 2025", daysLeft: 15, status: "upcoming" }
  ];

  const recentPayments = [
    { id: "PAY-R001", orderId: "ORD-2024-003", client: "Tech Solutions Pvt Ltd", amount: "₹45,500", paidOn: "Jan 05, 2025" },
    { id: "PAY-R002", orderId: "ORD-2024-005", client: "Premier Supplies", amount: "₹78,000", paidOn: "Dec 28, 2024" }
  ];

  $: totalUpcoming =
    upcomingPayments.reduce(
      (sum, p) => sum + Number(p.amount.replace(/[₹,]/g, "")),
      0
    );

  $: urgentCount = upcomingPayments.filter(p => p.status === "urgent").length;
</script>

<div class="space-y-8 animate-fade-in ml-6">
  <!-- HEADER -->
  <div>
    <h1 class="text-3xl font-bold">Payments</h1>
    <p class="text-gray-500 mt-1">Track upcoming and recent payments</p>
  </div>

  <!-- SUMMARY -->
  <div class="grid gap-4 md:grid-cols-3">
    <Card>
      <CardContent className="pt-6">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-sm text-gray-500">Total Upcoming</p>
            <p class="text-2xl font-bold mt-1">₹{totalUpcoming.toLocaleString()}</p>
          </div>
          <div class="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
            <CreditCard class="w-6 h-6 text-blue-600" />
          </div>
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardContent className="pt-6">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-sm text-gray-500">Pending Payments</p>
            <p class="text-2xl font-bold mt-1">{upcomingPayments.length}</p>
          </div>
          <div class="w-12 h-12 rounded-lg bg-yellow-100 flex items-center justify-center">
            <Clock class="w-6 h-6 text-yellow-600" />
          </div>
        </div>
      </CardContent>
    </Card>

    <Card>
      <CardContent className="pt-6">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-sm text-gray-500">Urgent (Due Soon)</p>
            <p class="text-2xl font-bold mt-1 text-red-600">{urgentCount}</p>
          </div>
          <div class="w-12 h-12 rounded-lg bg-red-100 flex items-center justify-center">
            <AlertCircle class="w-6 h-6 text-red-600" />
          </div>
        </div>
      </CardContent>
    </Card>
  </div>

  <!-- UPCOMING PAYMENTS -->
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center gap-2">
        <Calendar class="w-5 h-5 text-blue-600" />
        Upcoming Payments
      </CardTitle>
      <CardDescription>Payments due in the next 30 days</CardDescription>
    </CardHeader>

    <CardContent>
      <div class="space-y-4">
        {#each upcomingPayments as payment, i}
          <div
            class={`p-4 rounded-lg border transition-all animate-slide-in
              ${payment.status === "urgent"
                ? "border-red-300 bg-red-50"
                : "border-gray-200 bg-white hover:shadow"}`}
            style={`animation-delay:${i * 50}ms`}
          >
            <div class="flex flex-col sm:flex-row justify-between gap-4">
              <div class="flex gap-4">
                <div
                  class={`w-12 h-12 rounded-lg flex items-center justify-center
                  ${payment.status === "urgent" ? "bg-red-100" : "bg-blue-100"}`}
                >
                  <CreditCard
                    class={`w-6 h-6 ${payment.status === "urgent" ? "text-red-600" : "text-blue-600"}`}
                  />
                </div>

                <div>
                  <div class="flex items-center gap-2">
                    <p class="font-medium">{payment.client}</p>
                    {#if payment.status === "urgent"}
                      <Badge variant="destructive">Due Soon</Badge>
                    {/if}
                  </div>

                  <p class="text-sm text-gray-500 font-mono">{payment.orderId}</p>

                  <div class="flex gap-4 mt-2 text-sm">
                    <span class="text-gray-500">Due: {payment.dueDate}</span>
                    <span class={payment.daysLeft <= 3 ? "text-red-600 font-medium" : "text-gray-500"}>
                      {payment.daysLeft} days left
                    </span>
                  </div>
                </div>
              </div>

              <div class="flex items-center gap-4 pl-16 sm:pl-0">
                <p class="text-lg font-bold">{payment.amount}</p>
                <Button size="sm" variant="outline">Mark Paid</Button>
              </div>
            </div>

            {#if payment.status === "urgent"}
              <div class="mt-4">
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-gray-500">Payment deadline approaching</span>
                  <span class="text-red-600 font-medium">
                    {Math.round((1 - payment.daysLeft / 30) * 100)}%
                  </span>
                </div>
                <Progress value={(1 - payment.daysLeft / 30) * 100} />
              </div>
            {/if}
          </div>
        {/each}
      </div>
    </CardContent>
  </Card>

  <!-- RECENT PAYMENTS -->
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center gap-2">
        <CheckCircle class="w-5 h-5 text-green-600" />
        Recent Payments
      </CardTitle>
      <CardDescription>Successfully completed payments</CardDescription>
    </CardHeader>

    <CardContent>
      <div class="space-y-4">
        {#each recentPayments as payment, i}
          <div
            class="flex flex-col sm:flex-row justify-between gap-4 p-4 rounded-lg bg-green-50 border border-green-200 animate-slide-in"
            style={`animation-delay:${i * 50}ms`}
          >
            <div class="flex gap-4">
              <div class="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center">
                <CheckCircle class="w-6 h-6 text-green-600" />
              </div>
              <div>
                <p class="font-medium">{payment.client}</p>
                <p class="text-sm text-gray-500 font-mono">{payment.orderId}</p>
              </div>
            </div>

            <div class="flex gap-6 pl-16 sm:pl-0">
              <div class="text-sm">
                <p class="text-gray-500">Paid On</p>
                <p class="font-medium">{payment.paidOn}</p>
              </div>
              <div class="text-right">
                <p class="text-lg font-bold text-green-600">{payment.amount}</p>
                <Badge variant="success">Completed</Badge>
              </div>
            </div>
          </div>
        {/each}
      </div>
    </CardContent>
  </Card>
</div>
